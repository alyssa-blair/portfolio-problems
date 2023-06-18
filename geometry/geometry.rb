# A previous assignment which calculates the intersections of different geometry expressions
# All geometry expressions are immutable 
# Cannot use any functions to check which type of object is being intersected (such as is_a?)

# preprocess_prog - simplifies the expression if necessary 
# eval_prog - evaluates the expression under the current environment
# shift - shifts the expression 

class GeometryExpression
  Epsilon = 0.00001
end

class GeometryValue
  private
  def real_close(r1,r2)
    # checks if two coordinates are "the same" with floating point error
    (r1 - r2).abs < GeometryExpression::Epsilon
  end

  def real_close_point(x1,y1,x2,y2)
    # checks if two points are "the same" with floating point error
    real_close(x1,x2) && real_close(y1,y2)
  end

  def two_points_to_line(x1,y1,x2,y2)
    # check what kind of line it is
    if real_close(x1,x2)
      VerticalLine.new x1
    else
      m = (y2 - y1).to_f / (x2 - x1)
      b = y1 - m * x1
      Line.new(m,b)
    end
  end

  public
  def intersectNone none
    none
  end

  def intersectLineSegment seg
    line_result = intersect(two_points_to_line(seg.x1,seg.y1,seg.x2,seg.y2))
    line_result.intersectWithSegmentAsLineResult seg
  end
end

class None < GeometryValue
  # A none object, any intersection is also none
  def eval_prog env
    self
  end

  def preprocess_prog
    self
  end

  def shift(dx,dy)
    self
  end

  def intersect other
    other.intersectNone self
  end

  def intersectPoint p
    self
  end

  def intersectLine line
    self
  end

  def intersectVerticalLine vline
    self
  end

  def intersectWithSegmentAsLineResult seg
    self
  end
end


class Point < GeometryValue
  # A point with an x and y coordinate 
  attr_reader :x, :y
  def initialize(x,y)
    @x = x
    @y = y
  end

  def preprocess_prog
    self
  end

  def eval_prog env
    self
  end

  def shift(dx, dy)
    Point.new(@x+dx, @y+dy)
  end

  def inbetween(v, end1, end2) 
    (end1 - GeometryExpression::Epsilon <= v && v <= end2 + GeometryExpression::Epsilon) 
    || (end2 - GeometryExpression::Epsilon <= v && v <= end1 + GeometryExpression::Epsilon) 
  end 

  def intersect other
    other.intersectPoint self
  end

  def intersectPoint p 
    if real_close_point(p.x, p.y, @x, @y)
      self
    else
      None.new
    end
  end 

  def intersectLine l
    if real_close(((l.m * @x) + l.b), @y)
      self
    else 
      None.new
    end
  end 

  def intersectVerticalLine vl
    
    if real_close(vl.x, @x)
      self 
    else 
      None.new
    end
  end 

  def intersectNone none
    none
  end

  def intersectWithSegmentAsLineResult seg 
    if (inbetween(@x, seg.x1, seg.x2) && inbetween(@y, seg.y1, seg.y2))
      Point.new(@x, @y)
    else 
      None.new
    end
  end

end

class Line < GeometryValue
  # A line with a slope and y-intercept
  attr_reader :m, :b
  def initialize(m,b)
    @m = m
    @b = b
  end

  def shift (dx, dy)
    Line.new(@m, @b + dy - @m * dx)
  end 

  def intersect other
    other.intersectLine self
  end
  
  def preprocess_prog
    self
  end

  def eval_prog env
    self
  end

  def intersectPoint p
    if real_close((@m * p.x + @b), p.y)
      p
    else 
      None.new
    end
  end

  def intersectLine l
    if real_close(l.m, @m) && real_close(l.b, @b)
      self
    elsif real_close(l.m, @m)
      None.new 
    else
      x = (@b - l.b)/(l.m - @m)
      y = @m * x + @b
      Point.new(x, y)
    end
  end

  def intersectVerticalLine v
    Point.new(v.x, @m * v.x + @b)
  end

  def intersectWithSegmentAsLineResult seg
    seg
  end

end

class VerticalLine < GeometryValue
  # a vertical line with an x-coordinate
  attr_reader :x
  def initialize x
    @x = x
  end

  def shift (dx, dy) 
    VerticalLine.new(@x+dx)
  end 

  def preprocess_prog
    self
  end

  def eval_prog env
    self
  end

  def intersect other
    other.intersectVerticalLine self
  end

  def intersectPoint p
    if real_close(p.x, @x)
      p 
    else 
      None.new
    end
  end

  def intersectLine l
    Point.new(@x, (l.m * x) + l.b) 
  end

  def intersectVerticalLine l
    if real_close(l.x, @x)
      self
    else 
      None.new
    end
  end

  def intersectWithSegmentAsLineResult seg
    seg
  end
end

class LineSegment < GeometryValue
  # a line segment with two x and y coordinates
  attr_reader :x1, :y1, :x2, :y2
  def initialize (x1,y1,x2,y2)
    @x1 = x1
    @y1 = y1
    @x2 = x2
    @y2 = y2
  end

  def shift (dx, dy)
    LineSegment.new(@x1+dx, @y1+dy, @x2+dx, @y2+dy)
  end

  def preprocess_prog 
    if real_close(@x1, @x2) && real_close(@y1, @y2)
      Point.new(@x1, @y1)
    elsif real_close(@x1, @x2)
      if @y1 < @y2
        LineSegment.new(@x2, @y2, @x1, @y1)
      else
        LineSegment.new(@x2, @y1, @x1, @y2)
      end
    elsif @x1 > @x2
      self
    else
        LineSegment.new(@x2, @y2, @x1, @y1)
    end
  end

  def intersect l
    l.intersectLineSegment self
  end

  def eval_prog env
    self
  end

  def intersectPoint p
    if ((@x1 - GeometryExpression::Epsilon <= p.x && p.x <= @x2 + GeometryExpression::Epsilon) ||
      (@x2 - GeometryExpression::Epsilon <= p.x && p.x <= @x1 + GeometryExpression::Epsilon)) && 
      ((@y1 - GeometryExpression::Epsilon <= p.x && p.x <= @y2 + GeometryExpression::Epsilon) ||
      (@y2 - GeometryExpression::Epsilon <= p.x && p.x <= @y1 + GeometryExpression::Epsilon))
      p
    else
      None.new
    end
  end

  
  def intersectLine l
    l.intersectLineSegment self
  end

  def intersectVerticalLine vline
    vline.intersectLineSegment self
  end

  def intersectWithSegmentAsLineResult seg
    if real_close(@x1, @x2)
      # if both x values are the same, vertical line
      if seg.y1 < @y1
        seg1 = seg 
        seg2 = self
      else 
        seg1 = self 
        seg2 = seg 
      end 

      if real_close(seg1.y1, seg2.y2)
        Point.new(seg1.x1, seg1.y1)
      elsif seg1.y1 < seg2.y2
        None.new 
      elsif seg1.y2 < seg2.y2
        LineSegment.new(seg1.x1, seg1.y1, seg2.x2, seg2.y2)
      else 
        LineSegment.new(seg1.x1, seg1.y1, seg1.x2, seg1.y2)
      end
    else 
      # otherwise, non-vertical line
      if @x1 < seg.x1
        seg1 = self 
        seg2 = seg
      else 
        seg1 = seg 
        seg2 = self 
      end 

      if real_close(seg1.x1, seg2.x2)
        Point.new(seg1.x1, seg1.y1)
      elsif seg2.x2 > seg1.x1
        None.new 
      elsif seg1.x2 > seg2.x2 
        LineSegment.new(seg1.x1, seg1.y1, seg1.x2, seg1.y2)
      else 
        LineSegment.new(seg1.x1, seg1.y1, seg2.x2, seg2.y2)
      end
    end
  end

end


class Intersect < GeometryExpression
  # an intersection between two geometry expressions
  def initialize(e1,e2)
    @e1 = e1
    @e2 = e2
  end

  def preprocess_prog
    Intersect.new(@e1.preprocess_prog, @e2.preprocess_prog)
  end

  def eval_prog env
    (@e1.eval_prog env).intersect(@e2.eval_prog env)
  end
end

class Let < GeometryExpression
  # set variable to equal e1 and evaluate e2 under current environment 
  def initialize(s,e1,e2)
    @s = s # variable 
    @e1 = e1 # geometry expression 1
    @e2 = e2 # geometry expression 2
  end
  
  def preprocess_prog
    Let.new(@s, @e1.preprocess_prog, @e2.preprocess_prog)
  end

  def eval_prog env
    pr = env.assoc @s
    if not pr.nil?
      # delete the existing value from the environment
      env = env.delete(pr)
    end
    # add the new variable
    @e2.eval_prog(env.append([@s, @e1]))
  end

end

class Var < GeometryExpression
  # get the value of the variable if in the environment
  def initialize s
    @s = s # variable
  end

  def eval_prog env
    pr = env.assoc @s
    raise "undefined variable" if pr.nil?
    pr[1]
  end

  def preprocess_prog 
    self
  end

  
end

class Shift < GeometryExpression
  # shift of a geometry expression
  def initialize(dx,dy,e)
    @dx = dx # shift on x-axis
    @dy = dy # shift on y-axis 
    @e = e # geometry expression
  end

  def preprocess_prog
    Shift.new(@dx, @dy, @e.preprocess_prog) 
  end

  def eval_prog env
    (@e.eval_prog env).shift(@dx, @dy)
  end

  def shift (x, y)
    Shift.new(@dx + x, @dy + y, @e).eval_prog([])
  end

end

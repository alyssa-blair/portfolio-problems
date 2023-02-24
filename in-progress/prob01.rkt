#lang racket

;; ====================================== Answers ======================================

; 1.1: TODO
; takes a stream s and number n
; returns list of n values produced by order in s
; if n == 0 then return list
; otherwise add car to list and recurse with n - 1
(define (stream-for-n-steps st n)
  (if (= n 0) ; if there n = 0
    '(); return first element in the stream
    (let ([p (st)])
      (cons (car p) (stream-for-n-steps (cdr p) (- n 1)) )))) ; otherwise, add current first element to the list

; 1.2: TODO
; corresponds to fibonacci sequence
(define fibo-stream
  (letrec ([f (lambda (x y)
                (cons x (lambda () (f y (+ x y)))))
              ])
           (lambda () (f 0 1))))

; 1.3: TODO
; takes a function and a stream
; returns a stream of booleans for if value should be returned 
;(define (filter-stream f s)
 ; (letrec ([g (lambda (f s)
  ;         (let ([p (s)])
   ;          (if (f (car p))
    ;             (cons p (lambda () (g f (cdr p)))) ; if part of the filter, add to stream and recurse
     ;            (lambda () (g f (cdr p)))
      ;           )))])
  ;(lambda () (g f s))))

; turn the stream into a list
; if the list is empty, return empty list
; else, take the first element of the list and apply the function to it
; if its true, append to result of next iteration
; if not, go to next iteration without appending
(define (filter-stream f s)
  (let ([g (λ (x f s)
             (if (f (x))
                     (λ () (cons x (filter-stream f s)))
                     (λ () (filter-stream f s))))])
    (let ([p (s)])
      (λ () (g (car p) f (cdr p))))))

        
; 1.4: TODO
;(define create-stream #f) ; replace define with macro definition



;; ==================================== Test suite =====================================

(require rackunit)

;; Sample stream for testing stream-for-n-steps
(define nat-num-stream (letrec ([f (lambda (x) (cons x (lambda () (f (+ x 1)))))]) (lambda () (f 0))))

;;; Test create-stream macro
;(create-stream squares using (lambda (x) (* x x)) starting at 5 with increment 2)

(define tests
  (test-suite "Sample tests for A3 P1"
   (check-equal? (stream-for-n-steps nat-num-stream 10)
              '(0 1 2 3 4 5 6 7 8 9)
                 "stream-for-n-steps test")
   (check-equal? (stream-for-n-steps fibo-stream 10) 
                 '(0 1 1 2 3 5 8 13 21 34) 
                 "fibo-stream test")
   (check-equal? (stream-for-n-steps (filter-stream (lambda (i) (> i 5)) nat-num-stream) 5)
                 '(6 7 8 9 10)
                 "filter stream test")
   ;(check-equal? (stream-for-n-steps squares 5)
   ;              '(25 49 81 121 169)
   ;              "stream defined using a macro. only tests is return value")))

  ))

;; Run the tests
(require rackunit/text-ui)
(run-tests tests)

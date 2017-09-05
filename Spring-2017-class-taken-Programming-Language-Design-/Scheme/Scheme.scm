;==Yongjun Chen HW3
;==Student ID: 11529168
;==========1. (deepSum L) -15%
;first define a addup function to add the whole
;value in a list
(define (addup L) (cond
                    ((null? L) 0)
                    (else (+ (car L) (addup (cdr L))) )
                    ))

;define deepSum L which may call the addup function defined before
;Here we assume if L='( ) ==> 0
(define (deepSum L) (cond
                      ((null? L) 0)
                      ((null? (car L)) 0)
                      ((pair? (car L)) (+ (addup (car L)) (deepSum (cdr L))))
                      ((+ (car L) (deepSum (cdr L))))
                      ))

;==========2. (numbersToSum sum L) - 15%
(define (numbersToSum sum L)
    (cond
      ((null? L) '())
      ((< sum (car L)) '())
      (else (cons (car L) (numbersToSum (- sum (car L)) (cdr L))) )
      ))

;==========3. (isSorted L) - 15%
;Here we assume the input is a list only have number values
(define (isSorted L) (cond
                       ((= (length L) 0) #t)
                       ((= (length L) 1) #t)
                       ((> (car L) (car (cdr L))) #f)
                       (else (isSorted (cdr L)))
                       ))

;==========4. (mergeUnique2 L1 L2) - 10%
(define (mergeUnique2 l1 l2)
  (cond
      ((null? l1) l2)
      ((null? l2) l1)
      ((< (car l1) (car l2)) (cons (car l1) (mergeUnique2 (cdr l1) l2)))
      ((< (car l2) (car l1)) (cons (car l2) (mergeUnique2 l1 (cdr l2))))
      ((mergeUnique2 l1 (cdr l2)))
      ))

;==========5. (mergeUniqueN Ln) - 10%
;define fold function
(define (fold fcombine basecase L) 
   (cond
      ((null? L) basecase)
      (else (fcombine (car L) (fold fcombine basecase (cdr L))))
   ))
;define mergeUniqueN Function
(define (mergeUniqueN Ln)(fold mergeUnique2 '() Ln))

;==========6. (matrixMap f M) - 10%
(define (MatrixMap f L) (map (lambda (y) (map f y) )  L))

;==========7. (avgOdd L) - 10%
;define filter function
(define (filter pred L) (cond
                          ((null? L) '())
                          ((pred (car L)) (cons (car L) (filter pred (cdr L))) )
                          (else (filter pred (cdr l)))
                          ))
;define an addup function without using recuisive
(define (addup L) (fold + 0 L))
;define a function to check weather input is odd or not
(define (odd x) (odd? x))
;define the length function without using recursive
(define (step x y) (+ y 1))
(define (mylength L) (fold step 0 L))

;Finally define the avgOdd function
(define (avgOdd L)(/ (addup (filter odd L)) (mylength (filter odd L))))

;==========8. (unzip L) - 15%
(define (unzip L)
    (cond
      ((null? L) (list '() '()))
      (else (list (cons (car (car L)) (car (unzip (cdr L)))) (cons (car (cdr (car L))) (car (cdr (unzip (cdr L)))))))
      ))

;=====================test function=====================
;'(=========test function for value result=========)
(define (test1 result Label)(cond
                            ((= result Label) '(Pass))
                            (else '(Not Pass))
                            ))

;'(=========test function for list result=========)
(define (test2 functionresult Label)(cond
                            ((equal? (list functionresult) (list Label)) '(Pass))
                            (else '(Not Pass))
                            ))

;=================main function for test=================
'(==========main function for test==========)
;test1
'(=========1 DeepSum L(15%)=========)
'(testcase 1:)
(test1 (deepSum '(1 (2 3 4) (5) 6 7 (8 9 10) 11))  66)
'(testcase 2:)
(test1 (deepSum '()) 0)
'(testcase 3:)
(test1 (deepSum '((2 3 4) 1 (3))) 13)
;test2
'(=========2 NumbersToSum sum L(15%)=========)
'(testcase 1:)
(test2 (numbersToSum 100 '(10 20 30 40)) '(10 20 30 40)) 
'(testcase 2:)
(test2 (numbersToSum 30 '(5 4 6 10 4 2 1 5)) '(5 4 6 10 4))
;test3
'(=========3 IsSorted L(15%)=========)
'(testcase 1:)
(test2 (isSorted '(1 4 5 6 10)) #t)
'(testcase 2:)
(test2 (isSorted '(1 3 6 5 10)) #f)
'(testcase 3:)
(test2 (isSorted '(1)) #t)
;test4
'(=========4 MergeUnique2 L1 L2(10%)=========)
'(testcase 1:)
(test2 (mergeUnique2 '(4 6 7) '(3 5 7)) '(3 4 5 6 7))
'(testcase 2:)
(test2 (mergeUnique2 '(1 5 7) '(2 5 7)) '(1 2 5 7))
'(testcase 3:)
(test2 (mergeUnique2 '() '(3 5 7)) '(3 5 7))
;test5
'(=========5 MergeUniqueN Ln(10%)=========)
'(testcase 1:)
(test2 (mergeUniqueN '()) '())
'(testcase 2:)
(test2 (mergeUniqueN '((2 4 6) (1 4 5 6))) '(1 2 4 5 6))
'(testcase 3:)
(test2 (mergeUniqueN '((2 4 6 10) (1 3 6) (8 9))) '(1 2 3 4 6 8 9 10))
;test6
'(=========6 MatrixMap f M(10%)=========)
'(testcase 1:)
(test2 (matrixMap (lambda (x) (* x x)) '((1 2) (3 4)) ) '((1 4) (9 16)))
'(testcase 2:)
(test2 (matrixMap (lambda (x) (+ 1 x)) '((0 1 2) (3 4 5)) ) '((1 2 3) (4 5 6)))
'(testcase 3:)
(test2 (MatrixMap (lambda (x) (* x x)) '((1 2) (3 4) (5 6) (4 5) (3 4 5 6)) ) '((1 4) (9 16) (25 36) (16 25) (9 16 25 36)))

;test7
'(=========7 AvgOdd L(10%)=========)
'(testcase 1:)
(test1 (avgOdd '(1 2 3 4 5)) 3)
'(testcase 2:)
(test1 (avgOdd '(1 3 5)) 3)
'(testcase 3:)
(test1 (avgOdd '(1 2 4 6)) 1)
;test8
'(=========8 Unzip L(15%)=========)
'(testcase 1:)
(test2 (unzip '((1 2) (3 4) (5 6))) '((1 3 5) (2 4 6)))
'(testcase 2:)
(test2 (unzip '((1 "a") (5 "b") (8 "c"))) '((1 5 8) ("a" "b" "c")))
'(testcase 3:)
(test2 (unzip '(("A" "a") ("B" "b") ("C" "c"))) '(("A" "B" "C") ("a" "b" "c")))
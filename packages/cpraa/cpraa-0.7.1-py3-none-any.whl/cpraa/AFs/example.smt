; P(A) = 2 ∗ P(C)

(declare-fun p_A () Real)
(declare-fun p_C () Real)
(assert (= p_A (* 2 p_C)))


; P(A ∨ C | -B) ≥ 0.8
; P((A ∨ C) ∧ -B) ≥ 0.8 ∗ P(-B)
; P(A ∧ -B) + P(C ∧ -B) - P(A ∧ C ∧ -B) ≥ 0.8 ∗ P(-B)

(declare-fun p_A_nB () Real)
(declare-fun p_nB_C () Real)
(declare-fun p_A_nB_C () Real)
(declare-fun p_nB () Real)
(assert (>= (- (+ p_A_nB p_nB_C) p_A_nB_C) (* 0.8 p_nB)))
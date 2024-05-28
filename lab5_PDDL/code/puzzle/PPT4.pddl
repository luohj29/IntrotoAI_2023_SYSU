(define (problem PPT4)
 (:domain puzzle)

(:objects pos_11 pos_12 pos_13 pos_14
        pos_21 pos_22 pos_23 pos_24
        pos_31 pos_32 pos_33 pos_34
        pos_41 pos_42 pos_43 pos_44 -loc
        
        tile_1 tile_2 tile_3 tile_4 tile_5 tile_6 tile_7 tile_8
        tile_9 tile_10 tile_11 tile_12 tile_13 tile_14 tile_15 -num)
;initial
; 0 5 15 14
; 7 9 6 13
; 1 2 12 10
; 8 11 4 3

;
 (:init (blank pos_11) 
        (at tile_5 pos_12)
        (at tile_15 pos_13)
        (at tile_14 pos_14)
        (at tile_7 pos_21)
        (at tile_9 pos_22)
        (at tile_6 pos_23)
        (at tile_13 pos_24)
        (at tile_1 pos_31)
        (at tile_2 pos_32)
        (at tile_12 pos_33)
        (at tile_10 pos_34)
        (at tile_8 pos_41)
        (at tile_11 pos_42)
        (at tile_4 pos_43)
        (at tile_3 pos_44)
        
        
         (neighbor pos_11 pos_12) (neighbor pos_12 pos_11)
        (neighbor pos_12 pos_13) (neighbor pos_13 pos_12)
        (neighbor pos_13 pos_14) (neighbor pos_14 pos_13)
        
        (neighbor pos_21 pos_22) (neighbor pos_22 pos_21)
        (neighbor pos_22 pos_23) (neighbor pos_23 pos_22)
        (neighbor pos_23 pos_24) (neighbor pos_24 pos_23)
        
        (neighbor pos_31 pos_32) (neighbor pos_32 pos_31)
        (neighbor pos_32 pos_33) (neighbor pos_33 pos_32)
        (neighbor pos_33 pos_34) (neighbor pos_34 pos_33)
        
        (neighbor pos_41 pos_42) (neighbor pos_42 pos_41)
        (neighbor pos_42 pos_43) (neighbor pos_43 pos_42)
        (neighbor pos_43 pos_44) (neighbor pos_44 pos_43)
        
        (neighbor pos_11 pos_21) (neighbor pos_21 pos_11)
        (neighbor pos_12 pos_22) (neighbor pos_22 pos_12)
        (neighbor pos_13 pos_23) (neighbor pos_23 pos_13)
        (neighbor pos_14 pos_24) (neighbor pos_24 pos_14)
        
        (neighbor pos_21 pos_31) (neighbor pos_31 pos_21)
        (neighbor pos_22 pos_32) (neighbor pos_32 pos_22)
        (neighbor pos_23 pos_33) (neighbor pos_33 pos_23)
        (neighbor pos_24 pos_34) (neighbor pos_34 pos_24)
        
        (neighbor pos_31 pos_41) (neighbor pos_41 pos_31)
        (neighbor pos_32 pos_42) (neighbor pos_42 pos_32)
        (neighbor pos_33 pos_43) (neighbor pos_43 pos_33)
        (neighbor pos_34 pos_44) (neighbor pos_44 pos_34)
        )
    
 (:goal (and (at tile_1 pos_11)
            (at tile_2 pos_12)
            (at tile_3 pos_13)
            (at tile_4 pos_14)
            (at tile_5 pos_21)
            (at tile_6 pos_22)
            (at tile_7 pos_23)
            (at tile_8 pos_24)
            (at tile_9 pos_31)
            (at tile_10 pos_32)
            (at tile_11 pos_33)
            (at tile_12 pos_34)
            (at tile_13 pos_41)
            (at tile_14 pos_42)
            (at tile_15 pos_43))
)

;goal
; 1 2 3 4
; 5 6 7 8
; 9 10 11 12
; 13 14 15 0
)
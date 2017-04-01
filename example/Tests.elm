module Tests exposing (..)

import Test exposing (..)
import Expect


all : Test
all =
    describe "Homework 1" [
        describe "Addition" [
            test "1 @2" <|
                \() -> Expect.equal (1 + 1) 2
          , test "2 @2" <|
                \() -> Expect.equal (2 + 2) 4
          , test "3 @3" <|
                \() -> Expect.equal (-1 + 1) 0
          , test "4 @3" <|
                \() -> Expect.equal (1 + 1) 3
        ]
      , describe "Multiplication" [
            test "1 @3" <|
                \() -> Expect.equal (2 * 3) 6
          , test "2 @2" <|
                \() -> Expect.equal (2 * 3) 7
        ]
    ]

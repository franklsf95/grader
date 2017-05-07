port module Main exposing (..)

--import Tests
import THeaps_test 
import Test.Runner.Node exposing (run, TestProgram)
import Json.Encode exposing (Value)


main : TestProgram
main =
    run emit THeaps_test.all


port emit : ( String, Value ) -> Cmd msg

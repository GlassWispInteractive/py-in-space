{-# LANGUAGE ForeignFunctionInterface #-}
module PyInSpace where

import Foreign
import Foreign.C.Types

star_brightness_hs :: Int -> Int
star_brightness_hs z = 60 + mod z 190
star_brightness :: CInt -> CInt
star_brightness = fromIntegral . star_brightness_hs . fromIntegral
foreign export ccall star_brightness :: CInt -> CInt

player_pos_x_hs :: Int -> Int
player_pos_x_hs xunits = 32+7*xunits
player_pos_x :: CInt -> CInt
player_pos_x = fromIntegral . player_pos_x_hs . fromIntegral
foreign export ccall player_pos_x :: CInt -> CInt

-- how to return a 2-tuple...?
invader_pos_hs :: Int -> Int -> (Int, Int)
invader_pos_hs x y = (26+25*x, 45+10*y)
--invader_pos :: CInt -> CInt -> (CInt, CInt)
--invader_pos = fromIntegral . invader_pos_hs . fromIntegral
--foreign export ccall invader_pos :: CInt -> CInt -> (CInt, CInt)

new_shot_pos_x_hs :: Int -> Int
new_shot_pos_x_hs xunits = 55+7*xunits
new_shot_pos_x :: CInt -> CInt
new_shot_pos_x = fromIntegral . new_shot_pos_x_hs . fromIntegral
foreign export ccall new_shot_pos_x :: CInt -> CInt


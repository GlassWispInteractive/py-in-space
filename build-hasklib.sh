ghc -c -dynamic -fPIC hasklib.hs
ghc -o hasklib.so -shared -dynamic -fPIC hasklib.o -lHSrts-ghc7.4.2
rm hasklib_stub.h hasklib.o hasklib.hi


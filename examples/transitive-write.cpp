class TW {
  int *x;
public:
  TW() : x(new int(0)) {}
  void transitiveWrite() const { *x = 42; }
};

int main()
{
  const TW tw;
  tw.transitiveWrite();
  return 0;
}

void writeToArg(int *y) { *y = 17; }

int main()
{
  const int *x = new int(0);
  writeToArg(const_cast<int *>(x));
  return 0;
}

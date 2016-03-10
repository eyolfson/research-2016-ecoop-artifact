// illustrates mutable fields as described in Section 3
class Mutable {
  mutable int x;
public:
  Mutable() {}
  void mutator() const { x = 42; }
};

int main()
{
  const Mutable m;
  m.mutator();
  return 0;
}

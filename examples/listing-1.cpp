#include <iostream>
#include <unordered_map>

class A {
public:
  int id;
  A() {}
};

bool operator==(const A& lhs, const A& rhs) { return lhs.id == rhs.id; }

namespace std {
template <>
struct hash<A> {
  size_t operator()(const A& a) const { return hash<int>()(a.id); }
};
}

void writeId(A *pa) {
  pa->id = 5;
}

void evil(const A& a) {
  writeId(const_cast<A*>(&a));
}

int main()
{
  std::unordered_map<A, std::string> m;
  const A a;

  m.insert(std::make_pair(a, "Value"));
  evil(a);

  if (m.find(a) != m.end()) {
    std::cout << "Expected output!\n";
  }
  else {
    std::cout << "Unexpected output!\n";
  }

  return 0;
}

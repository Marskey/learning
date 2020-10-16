#include <iostream>
#include <tuple>
#include <variant>
#include <type_traits>
class CPlayer
{
public:
    int i = 123;
};

class mouduleA
{
public:
    explicit mouduleA(CPlayer& p) {
        std::cout << "A " << p.i <<std::endl;
    }
    int i = 1;
};

class mouduleB
{
public:
    explicit mouduleB(CPlayer& p) {
        std::cout << "B " << p.i <<std::endl;
    }
    int i = 2;
};

class mouduleC
{
public:
    explicit mouduleC(CPlayer& p) {
        std::cout << "C " << p.i <<std::endl;
    }
    int i = 3;
};

class mouduleD
{
public:
    explicit mouduleD(CPlayer& p) {
        std::cout << "C " << p.i <<std::endl;
    }
    int i = 3;
};

class mouduleE
{
public:
    explicit mouduleE(CPlayer& p) {
        std::cout << "C " << p.i <<std::endl;
    }
    int i = 3;
};

class mouduleF
{
public:
    explicit mouduleF(CPlayer& p) {
        std::cout << "C " << p.i <<std::endl;
    }
    int i = 3;
};

class mouduleG
{
public:
    explicit mouduleG(CPlayer& p) {
        std::cout << "C " << p.i <<std::endl;
    }
    int i = 3;
};

class mouduleH
{
public:
    explicit mouduleH(CPlayer& p) {
        std::cout << "C " << p.i <<std::endl;
    }
    int i = 3;
};

template<typename ...T>
struct ModulesStruct
{
    ModulesStruct(CPlayer&) {}

    template <typename REQ_MODULE>
    REQ_MODULE& get() {
        static_assert(false, "This module is not register");
    }
};

template <typename REQ_MODULE, typename REAL_MODULE, bool BOOL_TYPE, typename ...REST>
struct get_if
{
    static REQ_MODULE& value(REAL_MODULE& f, ModulesStruct<REST...>& r) {
        return r.get<REQ_MODULE>();
    }
};

template <typename REQ_MODULE, typename REAL_MODULE, typename ...REST>
struct get_if<REQ_MODULE, REAL_MODULE, true, REST...>
{
    static REQ_MODULE& value(REAL_MODULE& f, ModulesStruct<REST...>& r) {
        return f;
    }
};

template<typename MODULE, typename ...OTHER_MODULE>
struct ModulesStruct<MODULE, OTHER_MODULE...>
{
    ModulesStruct(CPlayer& player)
        : first(player)
        , rest(player)
    {}

    template <typename REQ_MODULE>
    REQ_MODULE& get() {
        return get_if<REQ_MODULE, MODULE, std::is_same<REQ_MODULE, MODULE>::value, OTHER_MODULE...>::value(first, rest);
    }

private:
    MODULE first;
    ModulesStruct<OTHER_MODULE...> rest;
};

template < typename T >
struct ModuleStructValue
{
    T value;
    ModuleStructValue(CPlayer& arg) : value(arg) {}
};

template <typename ...T >
struct ModuleStruct : ModuleStructValue<T>...
{
    ModuleStruct(CPlayer& args) : ModuleStructValue<T>(args)... {
    }

    template < typename M >
    M& get() {
        return ModuleStructValue<M>::value;
    }

    template < typename M >
    const M& get() const {
        return ModuleStructValue<M>::value;
    }

    template<typename G>
    void getAll(std::list<G*>& ref) {
        ref = { &(ModuleStructValue<T>::value)... };
    }
};

int main() {
    CPlayer player;
    auto *temp = new ModuleStruct<mouduleA
                          , mouduleC
                          , mouduleB
                          , mouduleD>(player);

    moduleAInterface& d = temp->get<mouduleA>();

    std::list<moduleBase*> m;
    temp->getAll<moduleBase>(m);
 
    return 0;
}

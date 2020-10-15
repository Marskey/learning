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
struct type_tuple_value
{
    T value;
    type_tuple_value(CPlayer& arg) : value(arg) {}
};

template < typename ...T >
struct type_tuple : type_tuple_value<T>...
{
    type_tuple(CPlayer& args) : type_tuple_value<T>(args)... {
        args.i = 0;
    }

    template < typename U >
    U& get() {
        return type_tuple_value<U>::value;
    }

    template < typename U >
    const U& get() const {
        return type_tuple_value<U>::value;
    }
};

int main() {
    CPlayer player;
    //auto mm = ModulesStruct<mouduleA
    //                        , mouduleB
    //                        , mouduleC
    //                        , mouduleD
    //                        , mouduleE
    //                        , mouduleF
    //                        , mouduleG
    //                       >({ player });

    ////auto& b = mm.get<mouduleB>();
    ////std::cout << b.i;
    ////auto& a = mm.get<mouduleA>();
    ////std::cout << a.i;
    //auto& c = mm.get<mouduleG>();
    //std::cout << c.i;

    auto temp = type_tuple<mouduleB
                          , mouduleC
                          , mouduleD>(player);

    auto& d = temp.get<mouduleC>();
 
    return 0;
}

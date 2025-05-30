#include <Windows.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

#include <vector>

struct vec_3
{
    float x, y, z;
};

struct vec_4
{
    float x, y, z, w;
};

class player
{
private:
    uint64_t hp;
    float shield;
    char name[64];
public:
    vec_4 pos;
    player(const char* name, uint64_t hp, float shield, vec_4 pos)
    {
        this->hp = hp;
        this->shield = shield;
        this->pos = pos;
        strcpy(this->name, name);
    }
    bool is_alive()
    {
        return this->hp > 0.0f;
    }
};

std::vector<int> get_empty_vector()
{
    return std::vector<int>{};
}

const char* say_hello()
{
    return "bonjour";
}

char& get_first_alpha()
{
    char a = 'A';
    return a;
}

template <class T>
T GetAverage(T a, T b)
{
    return (a + b) / 2;
}

vec_3 GetZeroVector3()
{
    vec_3 zero_vector;
    memset(&zero_vector, 0, sizeof(vec_3));

    return zero_vector;
}

// Function to get a zero vector 4
vec_4 get_zero_vector_4()
{
    vec_4 zero_vector;
    memset(&zero_vector, 0, sizeof(vec_4));

    return zero_vector;
}

player merge_player(player player_a, player player_b, uint32_t iterations)
{
    player player_c("Jhon", 100, 0, get_zero_vector_4());   // Make a new player

    for (size_t i = 0; i < iterations; i++)
    {
        if (player_a.is_alive() && player_b.is_alive())
        {
            player_c.pos.x = GetAverage(player_a.pos.x, player_b.pos.x);
            player_c.pos.y = GetAverage(player_a.pos.y, player_b.pos.y);
            player_c.pos.z = GetAverage(player_a.pos.z, player_b.pos.z);
            player_c.pos.w += i;
        }
    }

    return player_c;
}

constexpr static float get_magic_number(float a, float b) {
    return a * 0.612376 - b * 1.2023895;
}

uint32_t GetMaxFromTwoIntegers(uint32_t a, uint32_t b) {
    if (a > b)
        return a;
    return b;
}

void* SomeGlobalVariable;
uint64_t anotherWeirdVar;

void main()
{
    std::vector<player> player_list;

    constexpr float magic_number = get_magic_number(23.0, 222.0f);
    
    uint64_t value = 0;
    value += magic_number;
    value = magic_number + value;

    player bob("bob", 100, 0, get_zero_vector_4());
    player alice("alice", 50, 10, get_zero_vector_4());

    player_list.push_back(bob);
    player_list.push_back(alice);

    player main = merge_player(bob, alice, 2);
    printf("Main player :\n");
    printf("\tIs alive : %d\n", main.is_alive());
    printf("\tPosition : (%.1f, %.1f, %.1f, %.1f)\n", main.pos.x, main.pos.y, main.pos.z, main.pos.w);

    std::qsort(player_list.data(), player_list.size(), sizeof(player), [](void const* a, void const* b) { return 1; });

    player_list.pop_back();
    player_list.pop_back();

    player_list.push_back(main);

    printf("Player list size : %d\n", player_list.size());
}
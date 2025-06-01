class Vec3 {
    constructor(x, y, z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

class Vec4 {
    constructor(x, y, z, w) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.w = w;
    }
}

class Player {
    constructor(name, hp, shield, pos) {
        this._hp = hp;
        this._shield = shield;
        this.name = name;
        this.pos = pos;
    }

    isAlive() {
        return this._hp > 0;
    }
}

function getEmptyVector() {
    return [];
}

function sayHello() {
    return "bonjour";
}

const getFirstAlpha = () => {
    let a = 'A';
    return a;
};

function getAverage(a, b) {
    return (a + b) / 2;
}

function getZeroVector3() {
    return new Vec3(0.0, 0.0, 0.0);
}

function getZeroVector4() {
    return new Vec4(0.0, 0.0, 0.0, 0.0);
}

function mergePlayer(playerA, playerB, iterations) {
    let playerC = new Player("Jhon", 100, 0, getZeroVector4());

    for (let i = 0; i < iterations; i++) {
        if (playerA.isAlive() && playerB.isAlive()) {
            playerC.pos.x = getAverage(playerA.pos.x, playerB.pos.x);
            playerC.pos.y = getAverage(playerA.pos.y, playerB.pos.y);
            playerC.pos.z = getAverage(playerA.pos.z, playerB.pos.z);
            playerC.pos.w += i;
        }
    }

    return playerC;
}

function getMagicNumber(a, b) {
    return a * 0.612376 - b * 1.2023895;
}

function GetMaxFromTwoIntegers(a, b) {
    if (a > b) {
        return a;
    }
    return b;
}

// specific a js
function whatIsThis(x = (() => { return Math.random() > 0.5 ? 42 : "forty-two" })()) {
    let weird = { ["dynamic" + "Key"]: x };
    let result = (typeof weird.dynamicKey === "number") ? x * 2 : `${x}??`;
    return result;
}

(() => {
    let playerList = [];
    var vvv = 0;
    const ccc = 0;
    let magicNumber = getMagicNumber(23.0, 222.0);

    let value = 0;
    value += magicNumber;
    value = magicNumber + value;

    let bob = new Player("bob", 100, 0, getZeroVector4());
    let alice = new Player("alice", 50, 10, getZeroVector4());

    playerList.push(bob);
    playerList.push(alice);

    let mainPlayer = mergePlayer(bob, alice, 2);

    console.log("Main player:");
    console.log(`\tIs alive: ${mainPlayer.isAlive()}`);
    console.log(`\tPosition: (${mainPlayer.pos.x.toFixed(1)}, ${mainPlayer.pos.y.toFixed(1)}, ${mainPlayer.pos.z.toFixed(1)}, ${mainPlayer.pos.w.toFixed(1)})`);

    playerList.sort((a, b) => 1);

    playerList.pop();
    playerList.pop();

    playerList.push(mainPlayer);

    console.log(`Player list size: ${playerList.length}`);

    console.log(`What is this? ${whatIsThis()}`);
})();

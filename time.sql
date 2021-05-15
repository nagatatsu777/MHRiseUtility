DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Quest;
DROP TABLE IF EXISTS TimeRecord
CASCADE;
DROP TABLE IF EXISTS ArmorSet;
DROP TABLE IF EXISTS Skill
CASCADE;
DROP TABLE IF EXISTS TimeRecord
CASCADE;
-- Table for user
CREATE TABLE Users
(
    username varchar(15) not null,
    pass varchar(15) not null,
    userrole varchar(15) not null,
    primary key(username)
);
CREATE TABLE Quest
(
    questname varchar(100) not null,
    monster varchar(30) not null,
    questrank int(2) not null,
    primary key(questname)
);

CREATE TABLE ArmorSet
(
    id int not null
    AUTO_INCREMENT,
    weapon varchar
    (30),
    weaponname varchar
    (30),
    helm varchar
    (30),
    chest varchar
    (30),
    arm varchar
    (30),
    waist varchar
    (30),
    leg varchar
    (30),
    deco varchar
    (30),  
    primary key
    (id)
);
    CREATE TABLE Skill
    (
        skillid int
        AUTO_INCREMENT,
    armorid int not null,
    skillname varchar
        (30),
    skilllevel int
        (1),
    primary key
        (skillid)
);
        CREATE TABLE TimeRecord
        (
            questname varchar(100) not null,
            weapon varchar(20) not null,
            minute int(2) not null,
            seconds int(2) not null,
            uploaddate date not null,
            username varchar(15),
            armorid int not null,
            primary key(questname,weapon,username,armorid)
        );
        INSERT INTO users
        VALUES('me', 's', 'user');
        INSERT INTO users
        VALUES('s', 's', 'admin');
        INSERT INTO Quest
        VALUES('取り巻くつむじ風', 'オサイズチ', '4');
        INSERT INTO Quest
        VALUES('グルメモンスターズ', 'アオアシラ、クルルヤック', '4');
        INSERT INTO Quest
        VALUES('学べ！軽弩の型', 'ドスフロギィ、ドスバギィ', '4');
        INSERT INTO Quest
        VALUES('傘鳥円舞', 'アケノシルム', '4');
        INSERT INTO Quest
        VALUES('大場所寒冷群島', 'ヨツミワドウ', '4');
        INSERT INTO Quest
        VALUES('変幻せよ！剣斧の型', 'ウルクスス、フルフル', '4');
        INSERT INTO Quest
        VALUES('水と共に生きるもの', 'ロアルドロス', '5');
        INSERT INTO Quest
        VALUES('泥の中でも立ち上がれ', 'ボルボロス', '5');
        INSERT INTO Quest
        VALUES('一柿入魂', 'ビシュテンゴ', '5');
        INSERT INTO Quest
        VALUES('砂原の魔球にご注意を', 'ラングロトラx２', '5');
        INSERT INTO Quest
        VALUES('それは血となり毒となる', 'プケプケ', '5');
        INSERT INTO Quest
        VALUES('岩の上にも三年', 'バサルモス', '5');
        INSERT INTO Quest
        VALUES('女王に魅せられて', 'リオレイア', '5');
        INSERT INTO Quest
        VALUES('不穏の沼影', 'ジュラトドス', '5');
        INSERT INTO Quest
        VALUES('山河に一閃、響く雷鳴', 'ジンオウガ', '6');
        INSERT INTO Quest
        VALUES('冥途へ誘う歌声', 'イソネミクニ', '6');
        INSERT INTO Quest
        VALUES('琥珀色の牙を研ぐ', 'ベリオロス', '6');
        INSERT INTO Quest
        VALUES('頭上を飛び跳ねる脅威', 'トビカガチ', '6');
        INSERT INTO Quest
        VALUES('猛追、蛮顎竜', 'アンジャナフ', '6');
        INSERT INTO Quest
        VALUES('赤き双眸、夜陰を断つ', 'ナルガクルガ', '6');
        INSERT INTO Quest
        VALUES('天上に紅蓮咲く', 'リオレウス', '6');
        INSERT INTO Quest
        VALUES('妖艶なる舞', 'タマミツネ', '6');
        INSERT INTO Quest
        VALUES('雪鬼獣がやってくる', 'ゴシャハギ', '7');
        INSERT INTO Quest
        VALUES('鬼火を纏石モノ', 'マガイマガド', '7');
        INSERT INTO Quest
        VALUES('泥海へ手招く', 'オロミドロ', '7');
        INSERT INTO Quest
        VALUES('地底を駆ける角竜', 'ディアブロス', '7');
        INSERT INTO Quest
        VALUES('轟轟たる咆哮', 'ティガレックス', '7');
        INSERT INTO Quest
        VALUES('悪鬼羅刹', 'ラージャン', '7');
        INSERT INTO Quest
        VALUES('火吹き御前', 'ヤツカダキ', '7');
        INSERT INTO Quest
        VALUES('雷神', 'ナルハタタヒメ', '7');
        INSERT INTO Quest
        VALUES('古の幻影', 'オオナズチ', '7');
        INSERT INTO Quest
        VALUES('嵐に舞う黒い影', 'クシャルダオラ', '7');
        INSERT INTO Quest
        VALUES('炎国の王', 'テオテスカトル', '7');
        INSERT INTO Quest
        VALUES('爆鱗竜、再び飛来す', 'バゼルギウス', '7');
        INSERT INTO Quest
        VALUES('牛飲馬食、ヌシアオアシラ', 'ヌシアオアシラ', '7');
        INSERT INTO Quest
        VALUES('優美高妙、ヌシリオレイア', 'ヌシリオレイア', '7');
        INSERT INTO Quest
        VALUES('千紫万紅、ヌシタマミツネ', 'ヌシタマミツネ', '7');
        INSERT INTO Quest
        VALUES('ウツシ教官の挑戦状・其の一', 'オロミドロ、ジンオウガ', '7');
        INSERT INTO Quest
        VALUES('ウツシ教官の挑戦状・其の二', 'ゴシャハギ、ラージャン', '7');
        INSERT INTO Quest
        VALUES('ウツシ教官の挑戦状・其の三', 'マガイマガド、ナルガクルガ', '7');
        INSERT INTO ArmorSet
        VALUES('1', '太刀', '月刀　夜影', 'カイザー', 'ヴァイクS', 'レウスS', 'ジャナフS', 'ハンターS', '見切り４スロ３');
        INSERT INTO ArmorSet
        VALUES('2', 'ヘビィボウガン', '王牙砲［山雷］', 'カイザー', 'ヴァイクS', 'ヴァイクS', 'ジャナフS', 'ハンターS', '見切り４スロ３');
        INSERT INTO TimeRecord
        VALUES('学べ！軽弩の型', 'ヘビィボウガン', '2', '52', '2020-03-01', 'me', '1');


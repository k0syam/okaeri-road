# おかえりロード 〜天使とあくまのさんぽ道〜

CCFOLIA（[ccfolia.com](https://ccfolia.com/)）で遊べる、トランプ＋ダイスすごろく形式のチーム対戦ボードゲームです。

NPCを「太らせたいあくま陣営」と「痩せて健康にしたいてんし陣営」に分かれて、NPCが帰宅するまでにゲージを奪い合います。

- 対象人数：3〜6人（2チーム対抗）
- プレイ時間：約30分
- 必要なもの：CCFOLIAのルーム、トランプ1組、このリポジトリの画像素材

詳しいルールは [RULES.md](RULES.md) を参照してください。

## クイックスタート（CCFOLIAでの遊び方）

1. CCFOLIAでルームを作成し、プレイヤーを招待する。
2. シーンの背景画像として [`assets/board_route_gauge.png`](assets/board_route_gauge.png) をアップロードする。
3. [`assets/token_npc.png`](assets/token_npc.png) をNPC用コマとしてシーンに配置する（お好みで [`assets/token_angel.png`](assets/token_angel.png) / [`assets/token_devil.png`](assets/token_devil.png) / [`assets/token_gauge.png`](assets/token_gauge.png) も配置する）。
4. [`ccfolia/chat_palette.txt`](ccfolia/chat_palette.txt) の内容を各プレイヤーのチャットパレットにコピー＆ペーストする。
5. [RULES.md](RULES.md) に従ってセットアップし、プレイ開始。

## リポジトリ構成

```
okaeri-road/
├── README.md              このファイル
├── RULES.md                ゲームルール本体
├── assets/                 CCFOLIA用の画像素材
│   ├── board_route_gauge.png   すごろくボード＋体調ゲージ（背景画像用）
│   ├── board_route_gauge.svg   同・編集用SVGソース
│   ├── token_npc.png           NPCコマ
│   ├── token_angel.png         てんし陣営コマ
│   ├── token_devil.png         あくま陣営コマ
│   ├── token_gauge.png         体調ゲージ用マーカー
│   └── token_*.svg             各コマの編集用SVGソース
└── ccfolia/
    └── chat_palette.txt    CCFOLIAチャットパレット用テキスト
```

## ライセンス

このゲームのルール・テキスト・画像素材は [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/deed.ja)（パブリックドメイン相当）で公開します。自由に改変・再配布・商用利用していただいて構いません。

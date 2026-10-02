# おかえりロード 〜天使とあくまのさんぽ道〜

CCFOLIA（[ccfolia.com](https://ccfolia.com/)）だけで完結する、トランプ＋ダイスすごろく形式のチーム対戦ボードゲームです。**現物のトランプは不要**で、カードは「ディーラー役」が秘話（ないしょ話）で管理する仮想デッキで代用します。

NPCを「太らせたいあくま陣営」と「痩せて健康にしたいてんし陣営」に分かれて、分岐すごろくのルートとゲージを奪い合います。

- 対象人数：3〜6人（2チーム対抗＋中立のディーラー1名を推奨）
- プレイ時間：約40分
- 必要なもの：CCFOLIAのルーム、このリポジトリの画像素材（現物のトランプ・サイコロは不要）

詳しいルールは [RULES.md](RULES.md) を参照してください。

## クイックスタート（CCFOLIAでの遊び方）

1. CCFOLIAでルームを作成し、プレイヤーを招待する。
2. シーンの背景画像として [`assets/board_route_gauge.png`](assets/board_route_gauge.png) をアップロードする。
3. [`assets/token_npc.png`](assets/token_npc.png) をNPCコマとしてマス「1 スタート」に、[`assets/token_gauge.png`](assets/token_gauge.png) をゲージコマとして体調ゲージの「0」に配置する（お好みで陣営の目印として [`assets/token_angel.png`](assets/token_angel.png) / [`assets/token_devil.png`](assets/token_devil.png) も配置する）。
4. [`ccfolia/chat_palette.txt`](ccfolia/chat_palette.txt) の内容を各プレイヤーのチャットパレットにコピー＆ペーストする。
5. 中立の「ディーラー」役を1名決める（4人以上推奨。3人の場合は少人数ルールを使用）。
6. [RULES.md](RULES.md) に従ってセットアップし、プレイ開始。

## リポジトリ構成

```
okaeri-road/
├── README.md               このファイル
├── RULES.md                ゲームルール本体
├── IMPROVEMENT_LOG.md      自動改善ループの作業記録
├── LICENSE                 ライセンス（CC0 1.0）
├── assets/                 CCFOLIA用の画像素材
│   ├── board_route_gauge.png   すごろくボード＋体調ゲージ（背景画像用）
│   ├── board_route_gauge.svg   同・編集用SVGソース
│   ├── token_npc.png           NPCコマ
│   ├── token_angel.png         てんし陣営コマ
│   ├── token_devil.png         あくま陣営コマ
│   ├── token_gauge.png         体調ゲージ用マーカー
│   └── token_*.svg             各コマの編集用SVGソース
└── ccfolia/                CCFOLIA用のテキスト素材
    └── chat_palette.txt        CCFOLIAチャットパレット用テキスト
```

## ライセンス

このゲームのルール・テキスト・画像素材は [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/deed.ja)（パブリックドメイン相当）で公開します。自由に改変・再配布・商用利用していただいて構いません。

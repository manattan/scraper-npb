# scraper-npb
背番号の変遷が載っているwebサイトをスクレイピング&amp;DBに保存

http://sebango.web.fc2.com/

このウェブサイトにある, 各球団の背番号の変遷をスクレイピングし, いい感じの文字列に直しました.

team名, 背番号と共にpostgreSQLに保存しました.

例えば,  http://sebango.web.fc2.com/sebangou7/s-lions-sebangou7.html 

データがtableに保持されているので, trを探すことで取得. 比較的容易. 

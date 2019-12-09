create table chat_rooms(	
    id integer primary key autoincrement, 
    chat_room text unique);
	
create table users(
    id integer primary key autoincrement,
    username text,
    ip_address text,
    port integer);
	
create table messages (
	id integer primary key autoincrement,
	message text,
	chat_room_id integer,
	user_id integer,
	timestamp default current_timestamp,
	foreign key(user_id) references users(id),
	foreign key(chat_room_id) references chat_rooms(id));

create table chat_room_users(
	id integer primary key autoincrement,
	user_id integer,
	chat_room_id integer,
	foreign key(user_id) references users(id),
	foreign key(chat_room_id) references chat_rooms(id));


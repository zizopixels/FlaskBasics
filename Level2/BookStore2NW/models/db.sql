--****** mysql 数据库信息 ******--
-- 数据库名：bookstore
-- 数据库表：cart,users
-- 数据库链接用户：root
-- 数据库链接用户密码：root
******users表 保存用户信息******
create table users
(
  id         int unsigned auto_increment                        comment 用户id
    primary key,
  name       varchar(24)                         null,          comment 用户名
  email      varchar(64)                         null,          comment 用户邮箱地址
  tel        int                                 not null,      comment 用户手机号
  password   varchar(128)                        not null,      comment 用户手密码
  createtime timestamp default CURRENT_TIMESTAMP null,          comment 用户注册时间
  address_default varchar(24) null,                             comment 用户默认收货人信息对应mongodb数据库的_id
  constraint email
    unique (email),
  constraint tel
    unique (tel)
)
  charset = utf8;
******cart表 保存购物车物品信息******

CREATE TABLE IF NOT EXISTS `cart`(
   `id` INT  AUTO_INCREMENT PRIMARY KEY,                                    comment 购物车物品id
   `user_id` int unsigned,                                                  comment 物品所属用户id
   `book_id` VARCHAR(100)  ,                                                comment 图书id
   `book_num` VARCHAR(40)  ,                                                comment 图书数量
   `is_effe` int default 1,                                                 comment 是否有效
   `create_time` timestamp default CURRENT_TIMESTAMP null,                  comment 添加时间
   constraint `fk_cart_user` foreign key(user_id) references users(id)      comment 外键关联用户id
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


******admin表 保存后台管理员信息******

-- auto-generated definition
create table admin
(
  id           int auto_increment comment '自增id',
  email        varchar(64)   not null comment '登录邮箱地址',
  password     varchar(128)  not null comment '管理员登录密码',
  sign_count   int default 0 not null comment '登录次数',
  is_effective int default 1 not null comment '是否有效',
  last_signIn_time date          not null comment '上次登录时间',

  constraint admin_email_uindex
    unique (email),
  constraint admin_id_uindex
    unique (id)
)
  comment '管理员';

alter table admin
  add primary key (id);

--****************************** mongodb 数据库信息 ******************************************************************--
-- 数据库名：products
-- 集合：books,images,order,address
******books集合 保存图书信息******
books{
    _id         默认图书id
    img_url     图书图片url链接
    press       出版社
    pub_time    出版时间
    price       折后价格
    price_m     原价
    title       图书标题名
    subheading  简介
    author      作者
}
******images集合 保存图片数据******
images{
    _id     默认id
    name    图片名
    data    图片二进制数据
}
******order集合 保存订单信息******
order{
    _id             默认id
    order_no        订单号（年月日时分+七位随机数）
    amount          总价
    is_effective    是否有效
    is_processed    是否已处理
    user_id         订单用户id
    create_time     订单创建时间
    books[
        book_num    图书数量
        book_id     books集合中的图书id
    ]
}
******address集合 保存用户收货人信息******
address{
    _id             默认id
    name            收货人姓名
    tel             收货人手机号
    user_id         用户mysql数据库的user表id
    province        省份
    city            城市
    details         备注
}



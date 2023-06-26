// 以下是业务服务器API地址
// 本机开发时使用真机调试
// var WxApiRoot = 'http://39.102.36.135:8080/wx/';
// 局域网测试使用
var WxApiRoot = 'http://127.0.0.1:5000/';
// 云平台部署时使用
// var WxApiRoot = 'http://106.14.174.134:5000/';
// 云平台上线时使用
// var WxApiRoot = 'https://????';


module.exports = {
  Recommend: WxApiRoot + 'recommend/', //猜你喜欢接口--yes
  CatalogCurrent: WxApiRoot + 'catalog/current/', //分类目录当前分类数据接口--yes
  getSessionKeyByCode: WxApiRoot + 'auth/getSessionKeyByCode/', // getSessionKeyByCode--yes
  GoodsHistory: WxApiRoot + 'goods/history/',
  GoodsList: WxApiRoot + 'goods/list/', //获得商品列表--yes
  GoodsDetail: WxApiRoot + 'goods/detail/', //获得商品的详情--yes
  UpdateLike: WxApiRoot + 'like/update/',
  CheckLike: WxApiRoot + 'like/check',
  LikeList: WxApiRoot + 'like/index/', //获取收藏的数据--yes
  SearchResult: WxApiRoot + 'search/result/', //搜索结果--空数据
  UserIndex: WxApiRoot + 'user/index/', //个人页面用户相关信息--yes
};

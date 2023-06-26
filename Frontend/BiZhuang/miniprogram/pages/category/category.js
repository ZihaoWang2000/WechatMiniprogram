 
//引入本地json数据，这里引入的就是第一步定义的json数据
var jsonData = require('data.js');
Page({
  data: {
    //左侧的菜单数据
    leftMenuList:[],
    //右侧的商品/品牌数据
    rightContent:[],
    //被点击的左侧菜单
    currentIndex:0,
    // 右侧内容的滚动条距离
    scrollTop: 0
  },
  //接口的返回数据
  Cates:[],
  //我们在这里加载本地json数据
  onLoad: function () {
    this.getCates();
  },
  getCates(){
    //jsonData.dataList获取json.js里定义的json数据，并赋值给dataList
   this.Cates = jsonData.dataList[0].message;
   //构造左侧的大菜单数据
   let leftMenuList = this.Cates.map(v=>v.cat_name);
   //构造右侧的商品/品牌数据数据
   let rightContent = this.Cates[0].children;
   this.setData({
     leftMenuList,
     rightContent
   });
  },

  //左侧菜单的点击事件
  handleItemTap (e){
    /*
    1 获取被点击的标题身上的索引
    2 给data中的currentIndex赋值就可以了
    3 根据不同的索引来渲染右侧的商品内容
    */
   const {index} = e.currentTarget.dataset;
   let rightContent = this.Cates[index].children;
   this.setData({
     currentIndex:index,
     //重新设置右侧内容的scroll-view标签的距离顶部的距离
     rightContent,
     scrollTop:0
   })
  }
})
 
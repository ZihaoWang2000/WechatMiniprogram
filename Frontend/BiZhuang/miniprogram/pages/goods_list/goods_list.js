/*
1 用户上滑页面 滚动条触底，开始加载下一页数据
  1 找到滚动条触底时间
  2 判断有没有下一页数据
     1 获取到总页数 只有总条数
       总页数 = Math.ceil(总条数 pagetotal /页容量 pagesize)
     2 获取到当前页码
     3 判断一下 当前的页码是否大于等于 总页数
       表示没有下一页数据
  3 假如没有下一页数据 弹出一个提示
  4 假如还有下一页数据 来加载下一页数据
    1 当前的页码 ++
    2 重新发送请求
    3 数据请求回来 要对data中的数据进行拼接，而不是全部替换
*/
//引入本地json数据，这里引入的就是第一步定义的json数据
var util = require('../../utils/util.js');
var api = require('../../config/api.js');

Page({

  /**
   * 页面的初始数据
   */
  data: {
    tabs:[
      {
        id:0,
        value:"综合",
        isActive:true
      },
      {
        id:1,
        value:"价格",
        isActive:false
      }
    ],
    goodsList:[],
    cat_name:'',
    tabs_now:0
  },
//接口要的参数
QueryParams:{
  query:"", /*关键字*/
  gcat_id:"", /*商品类别id*/
  bcat_id:"", /*品牌类别id*/
  pagenum:1, /*第几页*/
  pagesize:10 /*页容量：每页请求的数据数目*/
},
//总页数
totalPages:1,

 //标题点击事件 从子组件传递过来
 handleTabsItemChange(e){
  //1 获取被点击的标题索引
  const {index} = e.detail;
  //2 修改源数组
  let {tabs} = this.data;
  tabs.forEach((v,i)=>i===index?v.isActive=true:v.isActive=false);
  // tabs_now: tabs.id;
  //3 赋值到data中
  this.setData({
    tabs
  });
  if (tabs[1].isActive){
    this.setData({
      tabs_now:tabs[1].id,
      pagenum: 1,
      goodsList:[]
    });
    this.getGoodsList(this.QueryParams.gcat_id,this.QueryParams.bcat_id,this.QueryParams.pagenum,this.QueryParams.pagesize,this.data.tabs_now);
    // console.log(this.data.tabs_now)
  };
  if (tabs[0].isActive){
    this.setData({
      tabs_now:tabs[0].id,
      pagenum: 1,
      goodsList:[]
    });
    this.getGoodsList(this.QueryParams.gcat_id,this.QueryParams.bcat_id,this.QueryParams.pagenum,this.QueryParams.pagesize,this.data.tabs_now);
    // console.log(this.data.tabs_now)
  }
},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.QueryParams.gcat_id = options.gcat_id;
    this.QueryParams.bcat_id = options.bcat_id;
    this.getGoodsList(this.QueryParams.gcat_id,this.QueryParams.bcat_id,this.QueryParams.pagenum,this.QueryParams.pagesize,this.data.tabs_now);
    this.setData({
      //拼接数组
      cat_name: '商品/品牌类型 > '+ options.cat_name
    })
  },

  //获取商品列表数据
  getGoodsList(gcat_id,bcat_id,pagenum,pagesize,tabs_now){
        wx.showLoading();
        util.request(api.CatalogCurrent, {
        gcat_id: gcat_id,
        bcat_id: bcat_id,
        pagenum: pagenum,
        pagesize: pagesize,
        tabs_now: tabs_now
      }, 'POST').then(res => {
          //获取 总条数
          const total = res.total; 
          //计算总页数
          this.totalPages = Math.ceil(total/this.QueryParams.pagesize);
          // console.log(this.totalPages);
          this.setData({
            //拼接数组
            goodsList: [...this.data.goodsList, ...res.goods]
          });
          wx.hideLoading()
      })
  },

  // loading
  showLoading: (msg = '加载中') => {
    wx.showLoading({
      title: msg,
      mask: true
    })
  },
 

  //页面上滑 滚动条触底事件
  onReachBottom(){
    // console.log("页面触底")
  // 1 判断还有没有下一页数据
    if(this.QueryParams.pagenum >= this.totalPages){
      // 没有下一页数据
      console.log('%c'+'没有下一页数据',"color:red;font-size:20px;bcakground-image:linear-gradient(to right,#0094ff,pink)");
    }else{
      //还有下一页数据
      // console.log('%c'+'还有下一页数据',"color:red;font-size:100px;bcakground-image:linear-gradient(to right,#0094ff,pink)");
      this.QueryParams.pagenum++;
      this.getGoodsList(this.QueryParams.gcat_id,this.QueryParams.bcat_id,this.QueryParams.pagenum,this.QueryParams.pagesize,this.data.tabs_now);
    }
  }
})
const app = getApp()
var util = require('../../utils/util.js');
var api = require('../../config/api.js');

Page({
  data: {
    show: true,
    goodsList:[],
    cat_name:'',
    goods_img:'',
    goods_name:'',
    goods_price:'',
    islike: false
  },

  //接口要的参数
QueryParams:{
  query:"", /*关键字*/
  item_id:"", /*类别id*/
  pagenum:1, /*第几页*/
  pagesize:10 /*页容量：每页请求的数据数目*/
},

  onLoad() {
    wx.setNavigationBarColor({
      frontColor: '#ffffff',
      backgroundColor: '#FA7298',
      animation: {
        duration: 400,
        timingFunc: 'easeIn'
      }
    })
    this.setData({
      dh: 740
    })

  },

    /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.QueryParams.item_id = options.item_id;
    this.getGoodsList(this.QueryParams.item_id,this.QueryParams.pagenum,this.QueryParams.pagesize);
    this.CheckLike()
  },

  //获取商品列表数据
  getGoodsList(item_id,pagenum,pagesize){
        wx.showLoading();
        util.request(api.GoodsDetail, {
        item_id: item_id,
        pagenum: pagenum,
        pagesize: pagesize
      }, 'POST').then(res => {
          //获取 总条数
          const total = res.total; 
          //计算总页数
          this.totalPages = Math.ceil(total/this.QueryParams.pagesize);
          // console.log(this.totalPages);
          this.setData({
            //拼接数组
            goodsList: [...this.data.goodsList, ...res.goods],
            goods_img: res.goods_img,
            goods_name: res.goods_name,
            goods_price:res.goods_price
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

  changeTabs(e) {
    const key = e.detail.activeKey;
    if (key === 'one') {
      this.setData({
        dh: 740
      })
    } else {
      this.setData({
        dh: 0
      })
    }

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
      this.getGoodsList(this.QueryParams.item_id,this.QueryParams.pagenum,this.QueryParams.pagesize);
    }
  },

  AddLike(){
    if (app.globalData.hasLogin){
      let item_id = this.QueryParams.item_id;
      let that = this;
      util.request(api.UpdateLike, {
        item_id: item_id,
        errno: 0
      }, 'POST').then(res => {
          that.setData({
            islike: true
          })
      })
    } else {
      wx.showToast({
        title: '请您先登录！',
        icon: 'none',
        duration: 1500
      })
    }
    
  },

  DeleteLike(){
    let item_id = this.QueryParams.item_id;
    let that = this;
    util.request(api.UpdateLike, {
      item_id: item_id,
      errno: 1
    }, 'POST').then(res => {
        that.setData({
          islike: false
        })
    })
  },

  CheckLike(){
    let item_id = this.QueryParams.item_id;
    let that = this;
    util.request(api.CheckLike, {
      item_id: item_id,
    }, 'POST').then(res => {
      console.log(res.errno)
      if (res.errno === 0){
        that.setData({
          islike: true
        })
      } else {
        that.setData({
          islike: false
        })
      }
    })
  },
})

// pages/home/home.js
const app = getApp();

var util = require('../../utils/util.js');
var api = require('../../config/api.js');
var user = require('../../utils/user.js');


Page({
  data:{
    banner:["cloud://cloud1-1gfk562j1135973f.636c-cloud1-1gfk562j1135973f-1305500910/image/home/banner1.jpg","cloud://cloud1-1gfk562j1135973f.636c-cloud1-1gfk562j1135973f-1305500910/image/home/banner2.jpg"],
    product_img:[],
    brand1:[{src:"cloud://cloud1-1gfk562j1135973f.636c-cloud1-1gfk562j1135973f-1305500910/image/home/logo1.png",name:"资生堂", bcat_id: 32},
    {src:"cloud://cloud1-1gfk562j1135973f.636c-cloud1-1gfk562j1135973f-1305500910/image/home/logo2.png",name:"自然堂", bcat_id: 40},
    {src:"cloud://cloud1-1gfk562j1135973f.636c-cloud1-1gfk562j1135973f-1305500910/image/home/logo3.jpg",name:"雅漾", bcat_id: 3},
    {src:"cloud://cloud1-1gfk562j1135973f.636c-cloud1-1gfk562j1135973f-1305500910/image/home/logo4.jpg",name:"香奈儿", bcat_id: 39}
    ],

    brand2:[{src:"cloud://cloud1-1gfk562j1135973f.636c-cloud1-1gfk562j1135973f-1305500910/image/home/logo6.png",name:"雅诗兰黛", bcat_id: 13},
    {src:"cloud://cloud1-1gfk562j1135973f.636c-cloud1-1gfk562j1135973f-1305500910/image/home/logo7.jpg",name:"科颜氏", bcat_id: 24},
    {src:"cloud://cloud1-1gfk562j1135973f.636c-cloud1-1gfk562j1135973f-1305500910/image/home/logo8.jpg",name:"古驰", bcat_id: 19},
    {src:"cloud://cloud1-1gfk562j1135973f.636c-cloud1-1gfk562j1135973f-1305500910/image/home/logo9.jpg",name:"阿玛尼", bcat_id: 16},
    {src:"cloud://cloud1-1gfk562j1135973f.636c-cloud1-1gfk562j1135973f-1305500910/image/home/logo10.jpg",name:"迪奥", bcat_id: 12}
    ],
    hasLogin: false,
    noData: false, // 商品数据是否加载结束
  },
  getUserProfile(e) {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认
    // 开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '用于完善会员资料', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        this.setData({
          userInfo: res.userInfo,
        })
        this.login()
      }
    })
  },
  
  login: function (e) {
    let that = this;
    wx.login({
      success(res) {
        util.request(api.getSessionKeyByCode, {
          code: res.code,
          user_info: that.data.userInfo
        }, 'POST').then(res => {
          if (res.errno === 0 || res.errno === 1) {
            wx.setStorageSync('openId', res.data.openid);
            that.setData({
              sessionKey: res.data.session_key,
              hasLogin: true,
            })
            wx.setStorageSync('userInfo', that.data.userInfo);
            wx.setStorageSync('token', res.data.session_key);
            app.globalData.hasLogin = true;
            // successToast("登录成功");
          }
        })
      }
    })
    console.log(that.data)
  },

  getRecommendList(){
    let that = this;
    let params = {
      'limit': 10
    };
    this.showLoading();
    util.request(api.Recommend, params,'POST').then(res => {
      console.log(res.data.goods_list)
      let _list = [];
      res.data.goods_list.forEach(item =>{
        // console.log(item); //这里的item就是从数组里拿出来的每一个每一组
        that.setData({
          url: item.url,
          name: item.name,
          price: item.price,
          item_id: item.item_id,
          goods_id: item.goods_id
        })
        _list.push(item)
      })
      this.setData({
        product_img: _list,
      });
      wx.hideLoading();
    });
  },
  
  onShow: function() {
    this.setData ({
      height:app.globalData.height
    });
    //获取用户的登录信息
    console.log(app.globalData.hasLogin)
    if (wx.getStorageSync('userInfo')) {
      // let userInfo = wx.getStorageSync('userInfo');
      this.setData({
        hasLogin: true
      });
      let that = this;
      util.request(api.UserIndex).then(function(res) {
         if (res.errno === 0) {
           that.setData({
            //  order: res.data.order,
            //  balanceMoney: res.data.balanceMoney,
            //  coupon: res.data.coupon,
            //  userIntegration: res.data.userIntegration,
           });
         }
       });
    } else {
      this.setData({
        hasLogin: false
      })
    }
    this.getRecommendList()
  },

  showLoading: (msg = '加载中') => {
    wx.showLoading({
      title: msg,
      mask: true
    })
  },
})

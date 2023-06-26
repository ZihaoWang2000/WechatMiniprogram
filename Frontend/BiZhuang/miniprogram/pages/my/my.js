// pages/my/my.js
const app = getApp();

var util = require('../../utils/util.js');
var api = require('../../config/api.js');
var user = require('../../utils/user.js');

Page({
  data: {
    userInfo: {
      nickName: '点击登录',
      avatarUrl: '../../images/userhead.png'
    },
    hasLogin: false,
  },
  getUserProfile(e) {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认
    // 开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '用于完善会员资料', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        console.log(res.userInfo)
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
              username: that.data.userInfo.nickName,
              userhead: that.data.userInfo.avatarUrl,
              hasLogin: true,
            })
            wx.setStorageSync('userInfo', that.data.userInfo);
            console.log(app.globalData.hasLogin)
            wx.setStorageSync('token', res.data.session_key);
            app.globalData.hasLogin = true;
            // app.globalData.tabBarCartNum = res.data.cartGoodsCount;
            // successToast("登录成功");
          }
        })
      }
    })
    console.log(that.data)
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onShow: function() {
    //获取用户的登录信息
    if (app.globalData.hasLogin) {
      let userInfo = wx.getStorageSync('userInfo');
      console.log(userInfo)
      this.setData({
        userInfo: userInfo,
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
  },

  goHelp: function() {
    wx.navigateTo({
      url: '/pages/help/help'
    });
  }
})
//app.js

var util = require('./utils/util.js');
var api = require('./config/api.js');
var user = require('./utils/user.js');

App({
  globalData : {
    height:0,
    hasLogin: false, // 是否登录
    tabBarLikeNum: 0, // tabBar 收藏数量
  },
  onLaunch: function (e) {
    // wx.setStorageSync('inviteId', e.query.co);
    wx.getShareInfo({shareTicket:e.shareTicket,
      success: function (res) {
      }
    });
// test
    const updateManager = wx.getUpdateManager();
    wx.getUpdateManager().onUpdateReady(function() {
      wx.showModal({
        title: '更新提示',
        content: '新版本已经准备好，是否重启应用？',
        success: function(res) {
          if (res.confirm) {
            // 新的版本已经下载好，调用 applyUpdate 应用新版本并重启
            updateManager.applyUpdate()
          }
        }
      })
    });
    wx.getSystemInfo({
      success: (result) => {
        this.globalData.height = result.statusBarHeight;
      },
    })
    console.log(this.globalData)
    if (!wx.cloud) {
      console.error('请使用 2.2.3 或以上的基础库以使用云能力')
    } else {
      wx.cloud.init({
        // env 参数说明：
        //   env 参数决定接下来小程序发起的云开发调用（wx.cloud.xxx）会默认请求到哪个云环境的资源
        //   此处请填入环境 ID, 环境 ID 可打开云控制台查看
        //   如不填则使用默认环境（第一个创建的环境）
        // env: 'my-env-id',
        traceUser: true,
      })
    }
  },
  onShow: function(options) {
    // debugger
    user.checkLogin().then(res => {
      this.globalData.hasLogin = true;
    }).catch(() => {
      this.globalData.hasLogin = false;
    });
  },
})

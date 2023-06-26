const app = getApp()
const query = wx.createSelectorQuery();

var util = require('../../utils/util.js');
var api = require('../../config/api.js');
var user = require('../../utils/user.js');

Page({
  data: {
    show: true,
    touchStartTime: 0,
    touchEndTime: 0,
    longShow: false,
    product_img:[],
    hasLogin: false,
    like_list:[],
    checked_all: false
  },
  touchStart(e){
    console.log(e)
    this.touchStartTime = e.timeStamp
  },
  touchEnd(e){
    var that = this;
    console.log(e)
    var id = e.currentTarget.dataset.name;
    console.log(id)
    this.touchEndTime = e.timeStamp
    const times = this.touchEndTime - this.touchStartTime;
    console.log('times:', times)
    if(times < 200){
      wx.navigateTo({
        url: '/pages/detail/detail?item_id='+id,
      })
    }
    if(times > 300){
      wx.showModal({
        title: '',
        content: '要取消收藏所选商品？',
        success: function(res) {
          if (res.confirm) {
            util.request(api.UpdateLike, {
              item_id: id,
              errno: 1
            }, 'POST').then(function(res) {
              if (res.errno === 0) {
                wx.showToast({
                  title: '删除成功',
                  icon: 'success',
                  duration: 2000
                });
                that.getLikeList();
              }
            });
          }
        }
      });
    }
  },
  getRecommendList(){
    let that = this;
    let params = {
      'limit': 4
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

  getLikeList(){
    let that = this;
    util.request(api.LikeList).then(res => {
       if (res.errno === 0) {
        if (res.data.likeList.length > 0) {
          let _list = [];
          console.log(res.data.likeList);
          res.data.likeList.forEach(item => {
            that.setData({
              url: item.url,
              name: item.name,
              price: item.price,
              item_id: item.item_id,
              goods_id: item.goods_id,
              checked: item.checked
            })
            _list.push(item)
          })
          this.setData({
            like_list: _list,
          });
        } else {
          this.setData({
            like_list: []
          })
        }
       }
     })
  },

  onLoad: function() {
    this.getRecommendList();
    this.getLikeList()
  },

  onShow: function() {
    this.getLikeList();
    //获取用户的登录信息
    console.log(app.globalData.hasLogin)
    if (app.globalData.hasLogin) {
      let userInfo = wx.getStorageSync('userInfo');
      console.log(userInfo)
      this.setData({
        userInfo: userInfo,
        hasLogin: true
      });
    } else {
      this.setData({
        hasLogin: false
      })
    }
  },

  showLoading: (msg = '加载中') => {
    wx.showLoading({
      title: msg,
      mask: true
    })
  },

  CheckAll(){
    let checked_all = this.data.checked_all;
    let that = this;
    if ( ! checked_all) {
      this.data.like_list.forEach(item => {
        item.checked = true
        console.log(item)
      });
      console.log(this.data.like_list)
      this.setData({
       like_list: this.data.like_list,
       checked_all: true
      })
    } else {
      this.data.like_list.forEach(item => {
        item.checked = false
        console.log(item)
      });
      console.log(this.data.like_list)
      this.setData({
       like_list: this.data.like_list,
       checked_all: false
      })
    }
  },

  CheckOne(e){
    var id = e.currentTarget.dataset.id
    console.log(id)
  },

  DeleteLike(){
    
  }
})

// pages/search/search.js

var searchValue =''
var app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    history:[{name:"兰蔻",url:"../content/content"},
    {name:"粉水",url:"../content/content"},
    {name:"欧莱雅",url:"../content/content"},
    {name:"口红",url:"../content/content"}],

    hot:[{name:"施华蔻",url:""},
    {name:"粉水",url:""}],

    centent_Show: true,
    searchValue: ''
    
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },
  
  searchValueInput: function (e) {
    var value = e.detail.value;
    this.setData({
      searchValue: value,
    });
    if (!value && this.data.productData.length == 0) {
      this.setData({
        centent_Show: false,
      });
    }
  },

  SearchConfirm:function(e){
    var that = this;
    wx.navigateTo({
      url: '/pages/search_content/search_content?query=' + that.data.searchValue
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  
})
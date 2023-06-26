const app = getApp()
var util = require('../../utils/util.js');
var api = require('../../config/api.js');
 
Page({ 
  data: { 
    option: null,
    priceList:[],
    goods_logo:'',
    goods_name:'',
    goods_price:'',
    store_name:'',
    plat_name:'',
    min_date:'' //最小价格日期 
  }, 
  

onLoad: function (options){ 
    wx.setNavigationBarColor({ 
      frontColor: '#ffffff', 
      backgroundColor: '#FA7298', 
      animation: { 
        duration: 400, 
        timingFunc: 'easeIn' 
      } 
    }) 
    wx.showLoading();
        util.request(api.GoodsHistory, {
        goods_id: options.goods_id
      }, 'POST').then(res => {
          //获取 总条数
          const option = res.option; 
          this.setData({
            option,
            goods_logo:res.goods_logo,
            goods_name:res.goods_name,
            goods_price:res.goods_price,
            priceList:res.price_list,
            store_name:res.store_name,
            plat_name:res.plat_name,
            min_date:res.min_date //最小价格日期
          });
          // console.log(option);
          wx.hideLoading()
      })
},

  // loading
  showLoading: (msg = '加载中') => {
    wx.showLoading({
      title: msg,
      mask: true
    })
  }

})
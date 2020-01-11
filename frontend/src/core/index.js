import Vue from "vue";
import VueStorage from "vue-ls";

import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.less";

Vue.use(Antd);
Vue.use(VueStorage, {
  namespace: "pro__", // key prefix
  name: "ls", // name variable Vue.[ls] or this.[$ls],
  storage: "local" // storage name session, local, memory
});

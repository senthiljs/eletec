<template>
  <page-view>
    <a-card
      :bordered="false"
      :bodyStyle="{ padding: '16px 0', height: '100%' }"
      :style="{ height: '100%' }"
    >
      <div class="account-settings-info-main" :class="device">
        <div class="account-settings-info-left">
          <a-menu
            :mode="device == 'mobile' ? 'horizontal' : 'inline'"
            :style="{
              border: '0',
              width: device == 'mobile' ? '560px' : 'auto'
            }"
            :defaultSelectedKeys="['1']"
            :selectedKeys="selectedKeys"
            type="inner"
            @openChange="onOpenChange"
          >
            <a-menu-item key="/admin/users/:id/profile">
              <router-link :to="{ name: 'UserProfile', id: $route.params.id }">
                Profile
              </router-link>
            </a-menu-item>
            <a-menu-item key="/admin/users/:id/contract">
              <router-link :to="{ name: 'UserContract', id: $route.params.id }">
                Contract
              </router-link>
            </a-menu-item>
            <a-menu-item key="/admin/users/:id/resource">
              <router-link :to="{ name: 'UserResource', id: $route.params.id }">
                Resource
              </router-link>
            </a-menu-item>
            <a-menu-item key="/admin/users/:id/address">
              <router-link :to="{ name: 'UserAddress', id: $route.params.id }">
                Address
              </router-link>
            </a-menu-item>
            <a-menu-item key="/admin/users/:id/skill">
              <router-link :to="{ name: 'UserSkill', id: $route.params.id }">
                Skill
              </router-link>
            </a-menu-item>
            <a-menu-item key="/admin/users/:id/worktime">
              <router-link :to="{ name: 'UserWorkTime', id: $route.params.id }">
                WorkTime
              </router-link>
            </a-menu-item>
          </a-menu>
        </div>
        <div class="account-settings-info-right">
          <!-- <div class="account-settings-info-title">
            <span>{{ $route.meta.title }}</span>
          </div>

          <a-divider></a-divider> -->
          <route-view></route-view>
        </div>
      </div>
    </a-card>
  </page-view>
</template>

<script>
import { RouteView, PageView } from "@/layouts";
import { mixinDevice } from "@/utils/mixin.js";

export default {
  components: {
    RouteView,
    PageView
  },
  mixins: [mixinDevice],
  data() {
    return {
      // horizontal  inline
      mode: "inline",

      openKeys: [],
      selectedKeys: []
    };
  },
  created() {
    this.updateMenu();
  },
  methods: {
    onOpenChange(openKeys) {
      this.openKeys = openKeys;
    },
    updateMenu() {
      const routes = this.$route.matched.concat();
      this.selectedKeys = [routes.pop().path];
    }
  },
  watch: {
    $route(val) {
      this.updateMenu();
    }
  }
};
</script>

<style lang="less" scoped>
.account-settings-info-main {
  width: 100%;
  display: flex;
  height: 100%;
  overflow: auto;

  &.mobile {
    display: block;

    .account-settings-info-left {
      border-right: unset;
      border-bottom: 1px solid #e8e8e8;
      width: 100%;
      height: 50px;
      overflow-x: auto;
      overflow-y: scroll;
    }
    .account-settings-info-right {
      padding: 20px 40px;
    }
  }

  .account-settings-info-left {
    border-right: 1px solid #e8e8e8;
    width: 224px;
  }

  .account-settings-info-right {
    flex: 1 1;
    padding: 8px 30px;

    .account-settings-info-title {
      color: rgba(0, 0, 0, 0.85);
      font-size: 20px;
      font-weight: 500;
      line-height: 28px;
      margin-bottom: 12px;
    }
    .account-settings-info-view {
      padding-top: 12px;
    }
  }
}
</style>

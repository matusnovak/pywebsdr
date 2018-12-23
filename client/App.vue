<template>
  <div id="app" class="h-100">
    <b-navbar toggleable="md" type="light" variant="light" class="mb-3 border-bottom box-shadow navbar">
      <b-container>
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand @click="$router.push('/')">PyWebSdr</b-navbar-brand>
        <b-collapse is-nav id="nav_collapse">

          <b-navbar-nav>
            <b-nav-item @click="$router.push('/listen')">Listen</b-nav-item>
            <b-nav-item href="#">Link #2</b-nav-item>
          </b-navbar-nav>

          <!-- Right aligned nav items -->
          <!-- <b-navbar-nav class="ml-auto">
            <b-nav-item-dropdown text="User" right>
              <b-dropdown-item @click="logout">Logout</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav> -->
        </b-collapse>
      </b-container>
    </b-navbar>

    <b-container>
      <router-view></router-view>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
    }
  },
  methods: {
  },
  mounted() {
		this.$nextTick(() => {
    })
  },
  components: {
  }
}
</script>

<style>
.navbar {
  background: #F6F6F6;
}
.border-top {
  border-top: 1px solid #e5e5e5;
}
.border-bottom {
  border-bottom: 1px solid #e5e5e5;
}
.box-shadow {
  box-shadow: 0 .25rem .75rem rgba(0, 0, 0, .05);
}
</style>
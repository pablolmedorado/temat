<template>
  <span class="text-h6 ml-3 mr-5">
    {{ konamiCodeActive ? "MiBeti" : appName }}
    <sub class="text-caption">{{ konamiCodeActive ? "1992" : version }}</sub>
  </span>
</template>

<script>
import { mapState } from "vuex";

import { version } from "@/../package.json";

export default {
  name: "AppLabel",
  data() {
    return {
      version
    };
  },
  computed: {
    ...mapState(["appName", "konamiCodeActive"])
  }
};
</script>

export default {
  inheritAttrs: false,
  props: {
    value: {
      type: Boolean,
      default: false
    },
    scrollable: {
      type: Boolean,
      default: true
    },
    persistent: {
      type: Boolean,
      default: false
    },
    maxWidth: {
      type: [String, Number],
      default: 700
    }
  },
  data() {
    return {
      showDialog: this.value
    };
  },
  watch: {
    value(newValue) {
      if (newValue) {
        this.open();
      } else {
        this.close();
      }
    },
    showDialog(newValue) {
      this.$emit("input", newValue);
    }
  },
  methods: {
    open() {
      this.showDialog = true;
    },
    close() {
      this.showDialog = false;
    }
  }
};

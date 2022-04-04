<template>
  <v-menu
    :disabled="!isTruncated"
    :close-on-content-click="false"
    :nudge-width="200"
    open-on-hover
    max-width="400px"
    offset-x
  >
    <template #activator="{ on, attrs }">
      <span :style="{ cursor }" v-bind="attrs" v-on="on">
        {{ truncatedText }}
      </span>
    </template>
    <v-card>
      <v-card-text class="text-pre-wrap">{{ text }}</v-card-text>
    </v-card>
  </v-menu>
</template>

<script>
import { computed, onMounted, ref } from "@vue/composition-api";
import { get, invoke } from "lodash-es";

import { truncate } from "@/utils/text";

export default {
  name: "TruncatedText",
  props: {
    value: {
      type: String,
      default: "",
    },
    textLength: {
      type: Number,
      default: 30,
    },
  },
  setup(props, { slots }) {
    // State
    const slotText = ref(null);

    // Computed
    const text = computed(() => props.value || slotText.value || "");
    const truncatedText = computed(() => truncate(text.value, props.textLength));
    const isTruncated = computed(() => text.value.length > props.textLength);
    const cursor = computed(() => (isTruncated.value ? "help" : "default"));

    // Lifecycle hooks
    onMounted(() => {
      const slotContent = invoke(slots, "default");
      slotText.value = get(slotContent, [0, "text"], null);
    });

    return {
      // Computed
      text,
      truncatedText,
      isTruncated,
      cursor,
    };
  },
};
</script>

<style scoped>
.text-pre-wrap {
  white-space: pre-wrap;
}
</style>

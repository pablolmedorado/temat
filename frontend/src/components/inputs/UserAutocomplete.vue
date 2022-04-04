<template>
  <v-autocomplete
    v-bind="{ ...$props, ...$attrs }"
    :items="userOptions"
    :item-text="(user) => `${user.first_name} ${user.last_name}`"
    item-value="id"
    :item-disabled="(user) => !user.is_active"
    :filter="filterFunction"
    :loading="!userOptions.length"
    v-on="$listeners"
  >
    <template v-if="multiple && truncateResults" #selection="{ item, index }">
      <v-chip v-if="index === 0" small>
        <span>{{ item.acronym }}</span>
      </v-chip>
      <span v-if="index === 1" class="grey--text text-caption">(+{{ value.length - 1 }} más)</span>
    </template>
    <template v-if="showRandomBtn && !readonly" #append-outer>
      <v-tooltip bottom>
        <template #activator="{ on, attrs }">
          <v-icon :disabled="disabled || readonly" v-bind="attrs" @click="getRandomUser" v-on="on">
            mdi-dice-multiple
          </v-icon>
        </template>
        <span> Selección aleatoria </span>
      </v-tooltip>
    </template>
    <template #item="{ item }">
      <v-list-item-avatar>
        <UserAvatar size="40" :font-size="14" :user="item" />
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>{{ `${item.first_name} ${item.last_name}` }}</v-list-item-title>
      </v-list-item-content>
    </template>
  </v-autocomplete>
</template>

<script>
import { computed } from "@vue/composition-api";
import { intersectionBy } from "lodash-es";

import { useUserStore } from "@/stores/users";

export default {
  name: "UserAutocomplete",
  inheritAttrs: false,
  props: {
    value: {
      type: [String, Number, Object, Array],
      default: null,
    },
    showRandomBtn: {
      type: Boolean,
      default: false,
    },
    items: {
      type: Array,
      default: () => [],
    },
    limitRandomChoicesTo: {
      type: Array,
      default: () => [],
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
    truncateResults: {
      type: Boolean,
      default: false,
    },
    returnObject: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { emit }) {
    // Store
    const userStore = useUserStore();

    // Computed
    const userOptions = computed(() => (props.items.length ? props.items : userStore.users));

    // Methods
    function filterFunction(item, queryText) {
      const fullText = `${item.acronym} ${item.first_name} ${item.last_name}`;
      return fullText.toLocaleLowerCase().indexOf(queryText.toLocaleLowerCase()) > -1;
    }
    function getRandomInt(max) {
      return Math.floor(Math.random() * Math.floor(max));
    }
    function getRandomUser() {
      let result;
      let choices = userOptions.value.filter((user) => user.is_active);
      if (props.limitRandomChoicesTo.length) {
        choices = props.returnObject
          ? intersectionBy(choices, props.limitRandomChoicesTo, "id")
          : choices.filter((user) => props.limitRandomChoicesTo.includes(user.id));
      }
      if (!choices.length) {
        result = null;
      } else {
        const randomIndex = getRandomInt(choices.length);
        result = props.returnObject ? choices[randomIndex] : choices[randomIndex].id;
      }
      emit("input", props.multiple ? [result] : result);
    }

    return {
      // Computed
      userOptions,
      // Methods
      filterFunction,
      getRandomUser,
    };
  },
};
</script>

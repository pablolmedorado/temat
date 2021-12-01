<template>
  <v-autocomplete
    v-bind="{ ...$props, ...$attrs }"
    :items="userOptions"
    :item-text="(user) => `${user.first_name} ${user.last_name}`"
    item-value="id"
    :item-disabled="(user) => !user.is_active"
    :disabled="disabled"
    :readonly="readonly"
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
import { mapState } from "vuex";
import { intersectionBy } from "lodash";

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
  computed: {
    ...mapState("users", {
      defaultUserList: "users",
    }),
    userOptions() {
      return this.items.length ? this.items : this.defaultUserList;
    },
  },
  methods: {
    getRandomInt(max) {
      return Math.floor(Math.random() * Math.floor(max));
    },
    getRandomUser() {
      let result;
      let choices = this.userOptions.filter((user) => user.is_active);
      if (this.limitRandomChoicesTo.length) {
        choices = this.returnObject
          ? intersectionBy(choices, this.limitRandomChoicesTo, "id")
          : choices.filter((user) => this.limitRandomChoicesTo.includes(user.id));
      }
      if (!choices.length) {
        result = null;
      } else {
        const randomIndex = this.getRandomInt(choices.length);
        result = this.returnObject ? choices[randomIndex] : choices[randomIndex].id;
      }
      this.$emit("input", this.multiple ? [result] : result);
    },
  },
};
</script>

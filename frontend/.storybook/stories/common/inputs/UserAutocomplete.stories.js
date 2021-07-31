import { action } from "@storybook/addon-actions";

import store from "@/store/index";

import UserAutocomplete from "@/components/inputs/UserAutocomplete";

export default {
  title: "Components/Common/Inputs/UserAutocomplete",
  component: UserAutocomplete,
  args: {
    items: [],
  },
  argTypes: {
    value: { table: { disable: true } },
  },
};

const Template = (args, { argTypes }) => ({
  store,
  components: { UserAutocomplete },
  props: Object.keys(argTypes),
  data() {
    return {
      user: null,
    };
  },
  methods: {
    onInput: action("input"),
  },
  template: `
    <UserAutocomplete
      v-model="user"
      label="User"
      v-bind="$props"
      @input="onInput"
    />
  `,
});

export const Default = Template.bind({});
Default.args = {
  items: [
    { id: 1, first_name: "Usuario", last_name: "Uno", acronym: "US1", is_active: true },
    { id: 2, first_name: "Usuaria", last_name: "Dos", acronym: "US2", is_active: true },
    { id: 3, first_name: "Usuarie", last_name: "Tres", acronym: "US3", is_active: false },
  ],
};

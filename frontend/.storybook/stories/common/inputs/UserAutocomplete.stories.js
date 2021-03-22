// Utilities
import { storyFactory } from "../../../util/helpers";
import { action } from "@storybook/addon-actions";
import { boolean, object } from "@storybook/addon-knobs";

// Store
import store from "@/store/index";

// Components
import UserAutocomplete from "@/components/common/inputs/UserAutocomplete";

export default { title: "Components/Common/Inputs/UserAutocomplete" };

const story = storyFactory({ UserAutocomplete });

const userList = [
  { id: 1, first_name: "Usuario", last_name: "Uno", acronym: "US1", is_active: true },
  { id: 2, first_name: "Usuario", last_name: "Dos", acronym: "US2", is_active: true },
  { id: 3, first_name: "Usuario", last_name: "Tres", acronym: "US3", is_active: false },
];

export const Default = () => {
  return story({
    store,
    props: {
      items: {
        default: object("Users", userList),
      },
      multiple: {
        default: boolean("Multiple", false),
      },
      truncateResults: {
        default: boolean("Truncate results", false),
      },
      showRandomBtn: {
        default: boolean("Enable random selection", true),
      },
      limitRandomChoicesTo: {
        default: object("Limit random choices to", []),
      },
      returnObject: {
        default: boolean("Return object", false),
      },
    },
    data() {
      return {
        user: null,
      };
    },
    methods: {
      input: action("input"),
    },
    template: `
      <UserAutocomplete
        v-model="user"
        label="User"
        :items="items"
        :multiple="multiple"
        :truncate-results="truncateResults"
        :show-random-btn="showRandomBtn"
        :limit-random-choices-to="limitRandomChoicesTo"
        :return-object="returnObject"
        clearable
        @input="input"
      />
    `,
  });
};

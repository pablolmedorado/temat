// Utilities
import { storyFactory } from "../../util/helpers";
import { object } from "@storybook/addon-knobs";

// Store
import store from "@/store/index";

// Components
import UserPill from "@/components/UserPill";

export default { title: "Components/Common/UserPill" };

const story = storyFactory({ UserPill });

const buildProps = () => ({
  user: {
    default: object("User", {
      acronym: "TUS",
      first_name: "Test",
      last_name: "User",
    }),
  },
});

export const Default = () => {
  store.commit("setKonamiCodeActive", false);
  return story({
    props: buildProps(),
    store,
    template: `
      <UserPill :user="user"></UserPill>
    `,
  });
};

export const KonamiCodeEnabled = () => {
  store.commit("setKonamiCodeActive", true);
  return story({
    props: buildProps(),
    store,
    template: `
      <UserPill :user="user"></UserPill>
    `,
  });
};

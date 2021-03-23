// Utilities
import { storyFactory } from "../../util/helpers";
import { boolean, number, object, text } from "@storybook/addon-knobs";

// Store
import store from "@/store/index";

// Components
import UserAvatar from "@/components/common/UserAvatar";

export default { title: "Components/Common/UserAvatar" };

const story = storyFactory({ UserAvatar });

const buildProps = () => ({
  user: {
    default: object("User", {
      acronym: "TUS",
      first_name: "Test",
      last_name: "User",
    }),
  },
  color: {
    default: text("Color", "teal"),
  },
  fontSize: {
    default: number("Font size", 14),
  },
  tooltip: {
    default: boolean("Show tooltip", true),
  },
});

export const Default = () => {
  store.commit("setKonamiCodeActive", false);
  return story({
    props: buildProps(),
    store,
    template: `
      <UserAvatar :user="user" :color="color" :font-size="fontSize" :tooltip="tooltip"></UserAvatar>
    `,
  });
};

export const KonamiCodeEnabled = () => {
  store.commit("setKonamiCodeActive", true);
  return story({
    props: buildProps(),
    store,
    template: `
      <UserAvatar :user="user" :color="color" :font-size="fontSize" :tooltip="tooltip"></UserAvatar>
    `,
  });
};

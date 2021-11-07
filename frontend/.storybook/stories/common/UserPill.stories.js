import store from "@/store/index";

import UserPill from "@/components/UserPill";

export default {
  title: "Components/Common/UserPill",
  component: UserPill,
  args: {
    user: {
      acronym: "TUS",
      first_name: "Test",
      last_name: "User",
    },
    activeKonamiCode: false,
  },
};

const Template = (args, { argTypes }) => {
  const { activeKonamiCode } = args;
  store.commit("setKonamiCodeActive", Boolean(activeKonamiCode));
  return {
    store,
    components: { UserPill },
    props: Object.keys(argTypes),
    template: `
      <UserPill v-bind="$props" />
    `,
  };
};

export const Default = Template.bind({});

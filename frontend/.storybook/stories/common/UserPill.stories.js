import { useMainStore } from "@/stores/main";

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
  const mainStore = useMainStore();
  const { activeKonamiCode } = args;
  mainStore.isKonamiCodeActive = Boolean(activeKonamiCode);
  return {
    components: { UserPill },
    props: Object.keys(argTypes),
    template: `
      <UserPill v-bind="$props" />
    `,
  };
};

export const Default = Template.bind({});

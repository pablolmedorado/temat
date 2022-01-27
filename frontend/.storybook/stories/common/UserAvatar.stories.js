import { useMainStore } from "@/stores/main";

import UserAvatar from "@/components/UserAvatar";

export default {
  title: "Components/Common/UserAvatar",
  component: UserAvatar,
  args: {
    user: {
      acronym: "TUS",
      first_name: "Test",
      last_name: "User",
    },
    color: "teal",
    fontSize: 14,
    tooltip: true,
    activeKonamiCode: false,
  },
};

const Template = (args, { argTypes }) => {
  const mainStore = useMainStore();
  const { activeKonamiCode } = args;
  mainStore.isKonamiCodeActive = Boolean(activeKonamiCode);
  return {
    components: { UserAvatar },
    props: Object.keys(argTypes),
    template: `
      <UserAvatar v-bind="$props" />
    `,
  };
};

export const Default = Template.bind({});

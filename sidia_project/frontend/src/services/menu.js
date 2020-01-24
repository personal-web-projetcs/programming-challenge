export async function getLeftMenuData() {
  return [
    {
      title: 'Settings',
      key: 'settings',
      icon: 'icmn icmn-cog utils__spin-delayed--pseudo-selector',
    },
    {
      divider: true,
    },
    {
      title: 'Dashboard',
      key: 'home',
      url: '/home/',
      icon: 'icmn icmn-home',
    },
    {
      title: 'Titles',
      key: 'list-titles',
      url: '/titles',
      icon: 'icmn icmn-menu',
    },
    {
      title: 'Top List',
      key: 'top-list',
      url: '/top-titles',
      icon: 'icmn icmn-menu',
    },
    {
      divider: true,
    },
    {
      title: 'Default Pages',
      key: 'defaultPages',
      icon: 'icmn icmn-file-text',
      children: [
        {
          key: 'register',
          title: 'Register',
          url: '/pages/register',
          pro: true,
        },
        {
          key: 'lockscreen',
          title: 'Lockscreen',
          url: '/pages/lockscreen',
          pro: true,
        },
      ],
    },
  ]
}
export async function getTopMenuData() {
  return [
    {
      title: 'Settings',
      key: 'settings',
      icon: 'icmn icmn-cog utils__spin-delayed--pseudo-selector',
    },
    {
      title: 'Dashboard',
      key: 'home',
      url: '/home/',
      icon: 'icmn icmn-home',
    },
    {
      title: 'Titles',
      key: 'list-titles',
      url: '/titles',
      icon: 'icmn icmn-menu',
    },
    {
      title: 'Top List',
      key: 'top-list',
      url: '/top-titles',
      icon: 'icmn icmn-menu',
    },
    {
      title: 'Default Pages',
      key: 'defaultPages',
      icon: 'icmn icmn-file-text',
      children: [
        {
          key: 'register',
          title: 'Register',
          url: '/pages/register',
          pro: true,
        },
        {
          key: 'lockscreen',
          title: 'Lockscreen',
          url: '/pages/lockscreen',
          pro: true,
        },
      ],
    },
  ]
}

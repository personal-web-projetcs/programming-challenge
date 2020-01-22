import React from 'react'
import { Typography } from 'antd'
import ProfileMenu from './ProfileMenu'
import LanguageSelector from './LanguageSelector'
import styles from './style.module.scss'

const { Title } = Typography;

class TopBar extends React.Component {
  render() {
    return (
      <div className={styles.topbar}>
        <div className="mr-4" style={{ marginTop: '1%' }}>
          <Title>Titles Management</Title>
        </div>
        <div className="mr-4" />
        <div className="mr-auto" />
        <div className="mr-4" />
        <div className="mr-4">
          <LanguageSelector />
        </div>
        <div className="mr-4" />
        <ProfileMenu />
      </div>
    )
  }
}

export default TopBar

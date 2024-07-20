import { MoonIconOutline, SunIconOutline } from '@neo4j-ndl/react/icons';
import { Typography, IconButton, Tabs, Switch, Button } from '@neo4j-ndl/react';
import React, { useState } from 'react';
import { ThemeWrapperContext } from '../../../context/ThemeWrapper';
import User from './User';
import "./header.css"

export default function Header({
  title,
  navItems = [],
  activeNavItem = navItems[0],
  setActiveNavItem = () => {},
  useNeo4jConnect = false,
  connectNeo4j = false,
  setConnectNeo4j = () => {},
  openConnectionModal = () => {},
  userHeader = true,
}: {
  title: string;
  navItems?: string[];
  activeNavItem?: string;
  setActiveNavItem?: (activeNavItem: string) => void;
  useNeo4jConnect?: boolean;
  connectNeo4j?: boolean;
  setConnectNeo4j?: (connectNeo4j: boolean) => void;
  openConnectionModal?: () => void;
  userHeader?: boolean;
}) {
  const themeUtils = React.useContext(ThemeWrapperContext);
  const [themeMode, setThemeMode] = useState<string>(themeUtils.colorMode);

  const toggleColorMode = () => {
    setThemeMode((prevThemeMode) => {
      return prevThemeMode === 'light' ? 'dark' : 'light';
    });
    themeUtils.toggleColorMode();
  };

  return (
    <div className='nav-bar n-bg-palette-neutral-bg-weak p-1 border-b-2 border-[rgb(var(--theme-palette-neutral-border-weak))] h-16'>
      <nav
        className='flex items-center justify-between'
        role='navigation'
        data-testid='navigation'
        id='navigation'
        aria-label='main navigation'
        
      >
        <section className='flex md:flex-row flex-col items-center w-1/6 shrink-0 grow-0'>
          <div className='md:inline-block'></div>
          <div className='flex justify-center md:ml-0 pl-0'>
            <Typography className='md:inline-block hidden' variant='h6'>
              {title}
            </Typography>
            <Typography className='md:hidden inline-block' variant='subheading-small'>
              {title}
            </Typography>
          </div>
        </section>

        <section className='flex w-1/3 shrink-0 grow-0 justify-center items-center mb-[-26px]'>
          <Tabs size='large' fill='underline' onChange={(e) => setActiveNavItem(e)} value={activeNavItem}>
            {navItems.map((item) => (
              <Tabs.Tab tabId={item} key={item}>
                {item}
              </Tabs.Tab>
            ))}
          </Tabs>
        </section>

        <section className='flex items-center justify-end w-1/6 grow-0'>
          <div className='flex grow-0 gap-x-1 w-max items-center pr-3'>
          <a className='getstarted-btn w-max' href='/foundation-preview'>Get started</a>
          </div>
          <div className='flex grow-0 gap-x-1 w-max items-center pr-3 text-light-neutral-bg-weak'>Login</div>
          <div className='min-w-max flex grow-0 gap-x-1 w-max items-center pr-3 text-light-neutral-bg-weak'>Contact Us</div>

          <div>
            <div className='flex grow-0 gap-x-1 w-max items-center pr-3'>
              {useNeo4jConnect ? (
                <Switch
                  checked={connectNeo4j}
                  onChange={(e) => {
                    if (e.target.checked) {
                      openConnectionModal();
                    } else {
                      setConnectNeo4j(false);
                    }
                  }}
                  disabled={false}
                  fluid={true}
                  label={`Connect${connectNeo4j ? 'ed' : ''} to Neo4j`}
                  labelBefore={true}
                />
              ) : null}
              <IconButton aria-label='Toggle Dark mode' clean size='large' onClick={toggleColorMode}>
                {themeMode === 'dark' ? (
                  <span role='img' aria-label='sun'>
                    <SunIconOutline />
                  </span>
                ) : (
                  <span role='img' aria-label='moon'>
                    <MoonIconOutline />
                  </span>
                )}
              </IconButton>
              {userHeader ? (
                <div className='hidden md:inline-block'>
                  <User />
                </div>
              ) : null}
            </div>
          </div>
        </section>
      </nav>
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import {
  EuiBadge,
  EuiButtonIcon,
  EuiContextMenuPanel,
  EuiContextMenuItem,
  EuiEmptyPrompt,
  EuiIcon,
  EuiInMemoryTable,
  EuiLink,
  EuiPopover,
  EuiSpacer,
  EuiSwitch,
  EuiText,
} from '@elastic/eui';
import MonitorService from 'services/monitors';

const MonitorAlertsEnabledButton: React.FC<{
  monitor: any;
  alertsEnabled: boolean;
}> = ({ monitor, alertsEnabled }) => {
  const [enabled, setEnabled] = useState(
    alertsEnabled && monitor.enabled
  );
  const [isPopoverOpen, setIsPopoverOpen] = useState(false);

  const closePopover = () => setIsPopoverOpen(false);

  const updateMonitorEnabled = async () => {
    const id = monitor.id;
    const body = { enabled: !enabled };

    setEnabled(!enabled);
    const resp = await MonitorService.update(id, body);
    // TODO: If err, change enabled back.
  };

  const handleClick = () => {
    if (alertsEnabled) {
      updateMonitorEnabled();
    } else {
      setIsPopoverOpen(!isPopoverOpen);
    }
  };

  const button = (
    <EuiSwitch label="" checked={enabled} onChange={handleClick} />
  );

  if (alertsEnabled) return button;

  return (
    <EuiPopover
      button={button}
      display="block"
      closePopover={closePopover}
      isOpen={isPopoverOpen}
    >
      To enable alerts, define a connector in{' '}
      <EuiLink
        onClick={() => {
          console.log('no-op');
        }}
      >
        Settings
      </EuiLink>
    </EuiPopover>
  );
};

const MonitorsTable: React.FC<{
  monitors: any;
  query: any;
  loading?: boolean;
}> = ({ monitors, query, loading }) => {
  const [message, setMessage] = useState(<>Loading monitors...</>);

  const [itemIdToOpenActionsPopoverMap, setItemIdToOpenActionsPopoverMap] =
    useState<{ [key: string]: boolean }>({});
    
  useEffect(() => {
    const emptyState = (
      <EuiEmptyPrompt
        title={<h3>No monitors found</h3>}
        titleSize="xs"
        body="Update the filters or create a monitor."
      />
    );

    if (monitors && monitors.length === 0) {
      setMessage(emptyState);
    } else {
      setMessage(<></>);
    }
  }, [monitors]);

  const togglePopover = (itemId: any) => {
    const isPopped: boolean = !itemIdToOpenActionsPopoverMap[itemId];
    const newItemIdToOpenActionsPopoverMap: any = {
      ...itemIdToOpenActionsPopoverMap,
      [itemId]: isPopped,
    };

    setItemIdToOpenActionsPopoverMap(newItemIdToOpenActionsPopoverMap);
  };

  const closePopover = (itemId: any) => {
    // only update the state if this item's popover is open
    if (isPopoverOpen(itemId)) {
      const newItemIdToOpenActionsPopoverMap: any = {
        ...itemIdToOpenActionsPopoverMap,
        [itemId]: false,
      };

      setItemIdToOpenActionsPopoverMap(newItemIdToOpenActionsPopoverMap);
    }
  };

  const isPopoverOpen = (itemId: any) => {
    return itemIdToOpenActionsPopoverMap[itemId];
  };

  const deleteMonitor = (itemId: any) => {
    const response = MonitorService.delete(itemId);
    // remove user from state based on response
    closePopover(itemId);

    window.location.reload();
  };

  const columns = [
    // {
    //   name: 'Status',
    //   render: (item: any) => {
    //     let color;

    //     switch (item.status) {
    //       case 'Healthy':
    //         color = 'success';
    //         break;
    //       case 'Unhealthy':
    //         color = 'danger';
    //         break;
    //       default:
    //         color = 'warning';
    //     }

    //     return (
    //       <div>
    //         <EuiBadge color={color}>{item.status}</EuiBadge>
    //         <EuiSpacer size="xs" />
    //         <EuiText size="s" color="subdued">
    //           <span>Checked {item.updated_at}</span>
    //         </EuiText>
    //       </div>
    //     );
    //   },
    // },
    {
      name: 'Name',
      render: (item: any) => {
        const monitor_type = item.type
          .split('_')
          .map((el: any) => {
            return el.charAt(0).toUpperCase() + el.slice(1);
          })
          .join(' ');

        return (
          <div>
            <EuiLink href={'/monitors/' + item.id}>
              <EuiText size="m">{item.name}</EuiText>
            </EuiLink>
            <EuiSpacer size="xs" />
            <EuiText size="s">{monitor_type}</EuiText>
          </div>
        );
      },
    },
    {
      field: 'datasource',
      name: 'Data Source',
      // render: (item: any) => {
      //   return (
      //     <>
      //       <EuiIcon type={item.type} size="l" />
      //       <EuiText style={{ marginLeft: 10 }}>
      //         {' '}
      //         <span>{item.name}</span>
      //       </EuiText>
      //     </>
      //   );
      // },
    },
    {
      name: 'Actions',
      render: (item: any) => {
        return (
          <EuiPopover
            id={`${item.id}-actions`}
            button={
              <EuiButtonIcon
                aria-label="Actions"
                iconType="gear"
                size="s"
                color="text"
                onClick={() => togglePopover(item.id)}
              />
            }
            isOpen={isPopoverOpen(item.id)}
            closePopover={() => closePopover(item.id)}
            panelPaddingSize="none"
            anchorPosition="leftCenter"
          >
            <EuiContextMenuPanel
              items={[
                <EuiContextMenuItem
                  key="C"
                  icon="trash"
                  onClick={() => {
                    deleteMonitor(item.id);
                  }}
                >
                  Delete
                </EuiContextMenuItem>,
              ]}
            />
          </EuiPopover>
        );
      },
    },
  ];

  return (
    <div className="searchDisplayNone">
      <EuiInMemoryTable
        search={{ query: query }}
        items={monitors}
        message={message}
        loading={loading}
        columns={columns}
        pagination={true}
      />
    </div>
  );
};

export default MonitorsTable;

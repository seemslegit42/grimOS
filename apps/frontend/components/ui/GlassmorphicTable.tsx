import { glassmorphicPanel } from '@/lib/glassmorphism';
import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

// Import from glasscn-ui
// Note: If these imports fail, you may need to adjust the import path based on your project setup
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from 'glasscn-ui/table';

interface GlassmorphicTableProps<T> {
  data: T[];
  columns: {
    key: string;
    header: ReactNode;
    cell: (item: T) => ReactNode;
    className?: string;
  }[];
  className?: string;
  onRowClick?: (item: T) => void;
  isLoading?: boolean;
  emptyState?: ReactNode;
}

export function GlassmorphicTable<T>({
  data,
  columns,
  className,
  onRowClick,
  isLoading = false,
  emptyState = <div className="py-8 text-center text-white/50">No data available</div>,
}: GlassmorphicTableProps<T>) {
  // Try to use shadcn/ui or glasscn-ui Table components if available
  try {
    return (
      <div className={cn(glassmorphicPanel({ variant: 'light' }), 'overflow-hidden', className)}>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader className="border-b border-white/10 bg-white/5">
              <TableRow>
                {columns.map((column) => (
                  <TableHead
                    key={column.key}
                    className={cn(
                      'px-4 py-3 text-left text-sm font-medium text-white/80',
                      column.className
                    )}
                  >
                    {column.header}
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody className="divide-y divide-white/5">
              {isLoading ? (
                // Loading state
                Array.from({ length: 5 }).map((_, index) => (
                  <TableRow key={`loading-${index}`} className="animate-pulse">
                    {columns.map((column) => (
                      <TableCell
                        key={`loading-${index}-${column.key}`}
                        className="px-4 py-3"
                      >
                        <div className="h-4 bg-white/10 rounded"></div>
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : data.length === 0 ? (
                // Empty state
                <TableRow>
                  <TableCell colSpan={columns.length} className="px-4 py-3">
                    {emptyState}
                  </TableCell>
                </TableRow>
              ) : (
                // Data rows
                data.map((item, index) => (
                  <TableRow
                    key={index}
                    className={cn(
                      'transition-colors',
                      onRowClick && 'cursor-pointer hover:bg-white/5'
                    )}
                    onClick={() => onRowClick?.(item)}
                  >
                    {columns.map((column) => (
                      <TableCell
                        key={`${index}-${column.key}`}
                        className={cn('px-4 py-3 text-sm text-white', column.className)}
                      >
                        {column.cell(item)}
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </div>
    );
  } catch (e) {
    // Fallback to standard HTML table if shadcn/ui or glasscn-ui components are not available
    return (
      <div className={cn(glassmorphicPanel({ variant: 'light' }), 'overflow-hidden', className)}>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/10 bg-white/5">
                {columns.map((column) => (
                  <th
                    key={column.key}
                    className={cn(
                      'px-4 py-3 text-left text-sm font-medium text-white/80',
                      column.className
                    )}
                  >
                    {column.header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {isLoading ? (
                // Loading state
                Array.from({ length: 5 }).map((_, index) => (
                  <tr key={`loading-${index}`} className="animate-pulse">
                    {columns.map((column) => (
                      <td
                        key={`loading-${index}-${column.key}`}
                        className="px-4 py-3"
                      >
                        <div className="h-4 bg-white/10 rounded"></div>
                      </td>
                    ))}
                  </tr>
                ))
              ) : data.length === 0 ? (
                // Empty state
                <tr>
                  <td colSpan={columns.length} className="px-4 py-3">
                    {emptyState}
                  </td>
                </tr>
              ) : (
                // Data rows
                data.map((item, index) => (
                  <tr
                    key={index}
                    className={cn(
                      'transition-colors',
                      onRowClick && 'cursor-pointer hover:bg-white/5'
                    )}
                    onClick={() => onRowClick?.(item)}
                  >
                    {columns.map((column) => (
                      <td
                        key={`${index}-${column.key}`}
                        className={cn('px-4 py-3 text-sm text-white', column.className)}
                      >
                        {column.cell(item)}
                      </td>
                    ))}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}
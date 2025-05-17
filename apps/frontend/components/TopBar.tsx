export function TopBar() {
  return (
    <header className="bg-gray-900 text-white p-4 flex justify-between items-center">
      <h1 className="text-lg font-bold">Grimoire</h1>
      <div>
        <button className="mr-4">Notifications</button>
        <button>Profile</button>
      </div>
    </header>
  );
}

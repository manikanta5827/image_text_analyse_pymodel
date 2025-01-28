import React, { useState } from "react";

const ResultDisplay = ({ result }) => {
  const [activeCategory, setActiveCategory] = useState(
    result?.categories?.[0] || ""
  );

  const handleCategoryClick = (category) => {
    setActiveCategory(category);

    const categoryElement = document.getElementById(category);
    if (categoryElement) {
      categoryElement.scrollIntoView({ behavior: "smooth" });
    }
  };

  if (!result || !result.categories || result.categories.length === 0) {
    return <div className="text-red-500">No data available to display.</div>;
  }

  return (
    <div className="mt-4">
      {/* Category Tabs */}
      <div className="flex gap-4 mb-6 overflow-x-auto">
        {result.categories.map((category) => (
          <button
            key={category}
            onClick={() => handleCategoryClick(category)}
            className={`py-2 px-4 rounded ${
              activeCategory === category
                ? "bg-blue-600 text-white shadow-md"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            {category}
          </button>
        ))}
      </div>

      {/* Items Display */}
      <div>
        {result.categories.map((category) => (
          <div key={category} id={category} className="mb-10">
            <h2 className="text-2xl font-bold text-blue-600 mb-4">{category}</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {result.items
                ?.filter((item) => item.category === category)
                ?.map((item, index) => (
                  <div
                    key={index}
                    className="border border-gray-300 rounded-lg p-4 shadow hover:shadow-lg transition-transform transform hover:scale-105"
                  >
                    {/* Item Details */}
                    <h3 className="text-xl font-semibold mb-2">{item.name}</h3>
                    <p className="text-gray-600 mb-2">{item.description}</p>

                    {/* Diet Badge */}
                    <p className="text-sm mt-2">
                      <span
                        className={`inline-block py-1 px-2 rounded ${
                          item.diet === "veg"
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >
                        {item.diet}
                      </span>
                    </p>

                    {/* Price */}
                    <p className="mt-2 text-lg font-bold text-blue-500">
                      ${item.price}
                    </p>

                    {/* Ingredients */}
                    {item.ingredients && (
                      <div className="mt-4">
                        <h4 className="font-semibold text-gray-700">Ingredients:</h4>
                        <ul className="list-disc list-inside text-gray-600">
                          {item.ingredients.map((ingredient, idx) => (
                            <li key={idx}>{ingredient}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Nutrition */}
                    {item.nutrition && (
                      <div className="mt-4">
                        <h4 className="font-semibold text-gray-700">Nutrition:</h4>
                        <div className="grid grid-cols-2 gap-2">
                          {Object.entries(item.nutrition).map(([key, value]) => (
                            <div
                              key={key}
                              className="bg-gray-100 p-2 rounded text-center shadow-sm"
                            >
                              <span className="block text-sm font-bold capitalize">
                                {key}
                              </span>
                              <span className="block text-sm">{value}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Spice Level */}
                    {item.spiceLevel && (
                      <div className="mt-4">
                        <h4 className="font-semibold text-gray-700">Spice Level:</h4>
                        <div
                          className={`py-1 px-3 inline-block rounded ${
                            item.spiceLevel === "low"
                              ? "bg-green-100 text-green-700"
                              : item.spiceLevel === "medium"
                              ? "bg-yellow-100 text-yellow-700"
                              : "bg-red-100 text-red-700"
                          }`}
                        >
                          {item.spiceLevel.charAt(0).toUpperCase() +
                            item.spiceLevel.slice(1)}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultDisplay;
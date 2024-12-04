``` javascript

import React, { useState, useCallback, useEffect } from 'react';
import { AlertCircle, Calendar, Cloud, MapPin, Utensils } from 'lucide-react';

// 모의 데이터 생성 함수들
const mockWeather = () => ({
    condition: "맑음",
    temperature: 23
});

const mockPlaces = () => ({
    places: [
        { name: "서울숲", type: "공원" },
        { name: "북촌한옥마을", type: "문화관광" }
    ]
});

const mockRestaurants = () => ({
    restaurants: [
        { name: "맛있는 식당", cuisine: "한식", rating: 4.5 },
        { name: "로맨틱 레스토랑", cuisine: "양식", rating: 4.8 }
    ]
});

// 모의 GPT 응답 생성
const mockGPTResponse = () => [
    "데이트 코스 추천:\n",
    "1. 오전 (10:00-12:00)\n",
    "   - 서울숲 산책\n",
    "   - 공원 내 카페에서 브런치\n",
    "2. 점심 (12:30-14:00)\n",
    "   - 맛있는 식당에서 한식 코스\n",
    "3. 오후 (14:30-17:00)\n",
    "   - 북촌한옥마을 관광\n",
    "4. 저녁 (18:00-20:00)\n",
    "   - 로맨틱 레스토랑에서 디너\n"
];

const DatePlanner = () => {
    const [loading, setLoading] = useState(false);
    const [messages, setMessages] = useState([]);
    const [currentStep, setCurrentStep] = useState(0);
    const [error, setError] = useState(null);

    const steps = [
        { icon: AlertCircle, text: '계획 수립 시작' },
        { icon: Cloud, text: '날씨 확인' },
        { icon: MapPin, text: '장소 탐색' },
        { icon: Utensils, text: '맛집 검색' },
        { icon: Calendar, text: '최종 계획 생성' }
    ];

    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    const addMessage = useCallback((message) => {
        setMessages(prev => [...prev, message]);
    }, []);

    const simulatePlanning = useCallback(async () => {
        try {
            // 날씨 정보
            addMessage("날씨 정보를 확인하고 있습니다...");
            await sleep(1000);
            const weather = mockWeather();
            addMessage(`날씨는 ${weather.condition}, 기온은 ${weather.temperature}도입니다.`);
            setCurrentStep(1);

            // 장소 정보
            await sleep(1000);
            addMessage("추천 장소를 찾고 있습니다...");
            const places = mockPlaces();
            places.places.forEach(place => {
                addMessage(`추천 장소: ${place.name} (${place.type})`);
            });
            setCurrentStep(2);

            // 레스토랑 정보
            await sleep(1000);
            addMessage("주변 맛집을 찾고 있습니다...");
            const restaurants = mockRestaurants();
            restaurants.restaurants.forEach(restaurant => {
                addMessage(`추천 식당: ${restaurant.name} (${restaurant.cuisine}, 평점: ${restaurant.rating})`);
            });
            setCurrentStep(3);

            // 최종 계획 생성
            await sleep(1000);
            addMessage("최종 데이트 코스를 생성하고 있습니다...");
            setCurrentStep(4);

            // GPT 응답 시뮬레이션
            const gptResponse = mockGPTResponse();
            for (const line of gptResponse) {
                await sleep(300);
                addMessage(line);
            }

            addMessage("계획 생성이 완료되었습니다.");

        } catch (error) {
            setError("계획 생성 중 오류가 발생했습니다.");
        } finally {
            setLoading(false);
        }
    }, [addMessage]);

    const startPlanning = useCallback(() => {
        setLoading(true);
        setMessages([]);
        setCurrentStep(0);
        setError(null);
        simulatePlanning();
    }, [simulatePlanning]);

    const handleRetry = () => {
        startPlanning();
    };

    return (
        <div className="w-full max-w-2xl mx-auto p-4 space-y-6">
            <div className="flex flex-col gap-4">
                <h1 className="text-2xl font-bold">데이트 플래너</h1>
                <div className="flex gap-4">
                    <button
                        onClick={startPlanning}
                        disabled={loading}
                        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
                    >
                        {loading ? '계획 생성 중...' : '데이트 계획 생성'}
                    </button>
                    {error && (
                        <button
                            onClick={handleRetry}
                            className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
                        >
                            다시 시도
                        </button>
                    )}
                </div>
            </div>

            {/* Progress Steps */}
            <div className="flex justify-between mb-8">
                {steps.map((step, index) => (
                    <div key={index} className="flex flex-col items-center">
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center
                            ${index <= currentStep ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
                            <step.icon size={20} />
                        </div>
                        <span className="text-sm mt-2">{step.text}</span>
                    </div>
                ))}
            </div>

            {/* Error Message */}
            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                    {error}
                </div>
            )}

            {/* Messages */}
            <div className="border rounded-lg p-4 min-h-[200px] bg-gray-50 relative">
                <div className="space-y-2">
                    {messages.map((message, index) => (
                        <div key={index} className="text-gray-700">
                            {message}
                        </div>
                    ))}
                </div>

                {loading && messages.length === 0 && (
                    <div className="absolute inset-0 flex items-center justify-center bg-gray-50 bg-opacity-90">
                        <div className="flex flex-col items-center gap-2">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
                            <p className="text-gray-500">계획을 생성하고 있습니다...</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DatePlanner;


```
